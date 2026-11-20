"""CLI entry point: scrape a topic, write a script, render a captioned short."""
import argparse
import os

from config import OUTPUT_DIR
from scraper import fetch_trending_topics
from script_generation import build_script, polish_with_forge
from templates import TEMPLATES, VIDEO_STYLES
from video_creation import render_video


def run(topic=None, template=None, style="default", use_forge=False):
    if topic:
        print(f"[topic] using supplied topic: '{topic}'")
    else:
        topics = fetch_trending_topics(limit=5)
        topic = topics[0]
        print(f"[topic] picked '{topic}' from {len(topics)} trending candidates")

    script = build_script(topic, template_name=template)
    print(f"[script] template='{script['template']}', {len(script['lines'])} lines")

    note = "template only (no LLM)"
    if use_forge:
        script, used_forge = polish_with_forge(script)
        note = "polished by Forge LLM" if used_forge else "Forge unreachable, kept template"
    print(f"[script] {note}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "short.mp4")
    render_video(script["lines"], output_path, style=style)
    print(f"[video] wrote {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Free pipeline: trending topic -> script template -> captioned video."
    )
    parser.add_argument("--topic", help="skip scraping and use this topic directly")
    parser.add_argument("--template", choices=list(TEMPLATES), help="pick a specific script template")
    parser.add_argument("--style", default="default", choices=list(VIDEO_STYLES), help="visual style")
    parser.add_argument(
        "--use-forge",
        action="store_true",
        help="polish the script with an OpenAI-compatible LLM (set FORGE_ENDPOINT, default is local Ollama)",
    )
    args = parser.parse_args()
    run(topic=args.topic, template=args.template, style=args.style, use_forge=args.use_forge)


if __name__ == "__main__":
    main()
