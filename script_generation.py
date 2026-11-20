"""Builds a video script from a topic using the template library, with an
optional LLM polishing pass."""
import random

from templates import TEMPLATES


def build_script(topic, template_name=None):
    """Fill a template with `topic` and return a script dict."""
    name = template_name or random.choice(list(TEMPLATES.keys()))
    if name not in TEMPLATES:
        raise ValueError(f"unknown template '{name}'; choices: {list(TEMPLATES)}")
    t = TEMPLATES[name]
    hook = t["hook"].format(topic=topic)
    body = [line.format(topic=topic) for line in t["body"]]
    cta = t["cta"].format(topic=topic)
    return {
        "topic": topic,
        "template": name,
        "hook": hook,
        "body": body,
        "cta": cta,
        "lines": [hook, *body, cta],
    }


def polish_with_forge(script, forge_call=None):
    """Optionally rewrite each line through an OpenAI-compatible LLM.

    `forge_call` is injectable (used by selftest.py with a canned reply, no
    network). Defaults to forge.call_forge, which talks to FORGE_ENDPOINT.
    Falls back to the unmodified template script if the model is unreachable
    or returns a mismatched number of lines.

    Returns (script, used_forge: bool).
    """
    if forge_call is None:
        from forge import call_forge as forge_call

    prompt = (
        "Rewrite each of the following short video-script lines to be punchier, "
        "same meaning, same number of lines, one rewritten line per output line, "
        "no numbering, no extra commentary:\n" + "\n".join(script["lines"])
    )
    reply = forge_call([{"role": "user", "content": prompt}])
    if not reply:
        return script, False

    new_lines = [line.strip() for line in reply.strip().splitlines() if line.strip()]
    if len(new_lines) != len(script["lines"]):
        return script, False

    polished = dict(script)
    polished["lines"] = new_lines
    polished["hook"] = new_lines[0]
    polished["body"] = new_lines[1:-1]
    polished["cta"] = new_lines[-1]
    return polished, True
