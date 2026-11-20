"""End-to-end self-test. No real LLM calls: the Forge-polish check uses a
canned, clearly-labelled reply instead of a network call. Network use (the
topic scraper) is limited to a public keyless API with one retry, and falls
back to a fixed local list on failure, so this still passes offline.

Prints "SELFTEST PASS" and exits 0 only if every check below passes.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

from scraper import fetch_trending_topics
from script_generation import build_script, polish_with_forge
from templates import TEMPLATES
from video_creation import render_video

# CANNED MODEL REPLY -- not a real LLM call, just a fixed string standing in
# for what a local Ollama server would return, so this test has no network
# or model dependency.
CANNED_MODEL_REPLY = (
    "Stop scrolling if this keeps wasting your week.\n"
    "Most people fumble it because they skip the setup.\n"
    "Do it the same repeatable way every single time.\n"
    "Nail the setup once, and it runs itself tomorrow.\n"
    "Follow for the rest of the playbook."
)


def canned_forge_call(messages, timeout=8):
    return CANNED_MODEL_REPLY


def dead_forge_call(messages, timeout=8):
    return None


def check(label, condition):
    print(f"[{label}] {'ok' if condition else 'FAIL'}")
    if not condition:
        raise AssertionError(label)


def main():
    # 1. Scraper: real call (keyless public API, one retry inside), falls
    # back to a fixed list offline -- either way it must return real topics.
    topics = fetch_trending_topics(limit=3)
    check("scraper returns topics", isinstance(topics, list) and len(topics) >= 1)
    check(
        "scraper topics are non-empty strings",
        all(isinstance(t, str) and t.strip() for t in topics),
    )

    # 2. Template library: every template fills in correctly.
    for name in TEMPLATES:
        script = build_script("meal prepping", template_name=name)
        check(
            f"template '{name}' has hook/body/cta/lines",
            all(k in script for k in ("hook", "body", "cta", "lines")),
        )
        check(
            f"template '{name}' substitutes the topic",
            any("meal prepping" in line.lower() for line in script["lines"]),
        )

    # 3. Forge polish path with a CANNED reply -- no network, no real model.
    base_script = build_script("cold email outreach", template_name="problem_solution")
    polished, used_forge = polish_with_forge(base_script, forge_call=canned_forge_call)
    check("forge polish reports it was used", used_forge is True)
    check("forge polish keeps the line count", len(polished["lines"]) == len(base_script["lines"]))
    check("forge polish actually changed the text", polished["lines"] != base_script["lines"])

    # 3b. Forge polish falls back cleanly when the model is unreachable.
    fallback, used_forge2 = polish_with_forge(base_script, forge_call=dead_forge_call)
    check(
        "forge fallback keeps the template script unchanged",
        used_forge2 is False and fallback["lines"] == base_script["lines"],
    )

    # 4. Video rendering: a real ffmpeg run producing a real, playable file.
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        print("[video render] skipped: ffmpeg/ffprobe not found on PATH")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = os.path.join(tmp, "test.mp4")
            lines = ["Line one of the test script.", "Line two wraps it up."]
            seconds_per_line = 1.0
            render_video(lines, out_path, width=320, height=240, fps=12, seconds_per_line=seconds_per_line)

            check("video file was created", os.path.exists(out_path) and os.path.getsize(out_path) > 0)

            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", out_path],
                capture_output=True,
                text=True,
                check=True,
            )
            duration = float(json.loads(probe.stdout)["format"]["duration"])
            expected = len(lines) * seconds_per_line
            check("video duration matches script length", abs(duration - expected) < 0.5)

    print("SELFTEST PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"SELFTEST FAIL: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"SELFTEST FAIL (unexpected error): {e}")
        sys.exit(1)
