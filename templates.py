"""The workflow library: script structures and visual styles.

Each script template is a hook / body / call-to-action skeleton with
`{topic}` placeholders. Add your own template dict here to extend the
library -- the shape is validated by selftest.py.
"""

TEMPLATES = {
    "problem_solution": {
        "hook": "Stop scrolling if {topic} has ever wasted your time.",
        "body": [
            "Here's why {topic} usually goes wrong: people skip the setup and wing it.",
            "Here's the fix: do {topic} the same repeatable way every time.",
            "Set it up once, and {topic} runs itself tomorrow.",
        ],
        "cta": "Follow for more on {topic}.",
    },
    "listicle": {
        "hook": "Three things nobody tells you about {topic}.",
        "body": [
            "One: {topic} takes longer than you think on the first try.",
            "Two: the second time is always faster.",
            "Three: write it down, or you will relearn {topic} from scratch.",
        ],
        "cta": "Save this before you try {topic} again.",
    },
    "myth_bust": {
        "hook": "You've been told {topic} requires expensive tools. It doesn't.",
        "body": [
            "The myth: {topic} needs a big budget to get right.",
            "The truth: {topic} needs a checklist, not a credit card.",
            "Use what you already have, and start {topic} today.",
        ],
        "cta": "Comment if you want the {topic} checklist.",
    },
}

# Visual templates for the renderer: background/text colors per style.
VIDEO_STYLES = {
    "default": {"bg_color": "0x1b1f24", "text_color": "white"},
    "alt": {"bg_color": "0x101820", "text_color": "0xffcc00"},
    "light": {"bg_color": "0xf4f1ea", "text_color": "0x1b1f24"},
}
