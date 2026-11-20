# AI Video Marketing Playbook

An Instagram account posted that one founder lets Codex handle the topic, script, and editing for short videos, and that his inbox is now too full to answer everyone who comments "PLAYBOOK." The usual move after that is a DM funnel. My move is different: build the actual pipeline and give it away.

So that's what this is. `video-marketing-automation` is a free, open-source rebuild of the same shape — topic in, edited video out — using only things anyone can run today. A scraper pulls a real trending topic from a public, keyless API (Hacker News front page, no login, no scraping behind a wall). A template library turns that topic into a hook/body/call-to-action script, with three structures to start from. An optional local LLM pass (Ollama by default, any OpenAI-compatible endpoint if you want) can punch up the wording, but the thing works completely without one. Then ffmpeg — real video editing, not a metaphor for it — renders the script into a captioned vertical video and stitches the clips together.

It is not a voiceover generator, not a stock-footage editor, and not a tool that logs into anything or DMs anyone. It makes no claim about what any video earns. What it claims is narrower and checkable: this part of the pipeline — topic, script, edit — runs for free, in an afternoon, with an API key you don't even need.

Grab it here: https://github.com/warboy176/video-marketing-automation

If this is useful enough that people want a real V2 — better templates, a proper font/style system, maybe a TTS hook — I'll build that version properly, and it'll be a paid tier. Not before. Free stays free until it's worth more than that.

Witness me.
