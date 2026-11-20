<img src="cover.png" alt="video-marketing-automation" width="100%">

# video-marketing-automation

**A free, open rebuild of the "AI runs my video marketing" pipeline — no paid API, no DM funnel.**

An Instagram account (li.workflow) is running a comment-"PLAYBOOK"-for-DM funnel claiming one founder lets Codex handle the topic, script, and editing for short videos that "bring in customers," and that his inbox is now too full to answer everyone. Maybe true, maybe not — there's no way to check from a post. What *is* checkable is whether the actual pipeline (topic → script → edited video) can be built for free with open tools. It can. This is that pipeline: a real trending-topic scraper, a script-template library, and an ffmpeg-based video renderer, chained together in about 250 lines of Python.

## What it does

- **Scrapes a topic.** `scraper.py` pulls current front-page titles from the Hacker News public API (keyless, no login) as a stand-in trend source, with one retry and a fixed offline fallback list.
- **Writes a script.** `script_generation.py` fills a hook/body/call-to-action template from `templates.py` with that topic. Three templates ship out of the box: `problem_solution`, `listicle`, `myth_bust`.
- **Optionally polishes it with an LLM.** If you run a local model (Ollama by default) and pass `--use-forge`, the script gets rewritten through it. Without one, you still get a complete script — the templates do the work.
- **Edits the video.** `video_creation.py` turns each script line into a timed caption on a solid-color background with ffmpeg, then concatenates the clips into one silent vertical mp4.

## Run it

```
python3 main.py
python3 main.py --topic "home espresso setup" --template listicle --style alt
python3 main.py --use-forge   # polish with a local Ollama server at FORGE_ENDPOINT
python3 selftest.py
```

You need `ffmpeg` on your PATH (`apt install ffmpeg` or `brew install ffmpeg`). Nothing else to install — the rest is Python 3.10+ standard library.

## What it is not

- Not a voiceover generator. There's no text-to-speech here; output is captioned slides, silent.
- Not a stock-footage editor. Backgrounds are solid colors from `templates.VIDEO_STYLES`, not b-roll.
- Not a social-trend scraper. It does not log into or scrape Reddit, Twitter/X, TikTok, or anything behind a login wall — that breaks platform rules and this project doesn't do it.
- Not a DM or spam tool, and it never posts anywhere automatically.
- Not tied to Codex or any paid API. The optional LLM step talks to any OpenAI-compatible endpoint, Ollama by default, at zero cost.

## The honest limits

- "Trending" means Hacker News front-page titles. That's a real, live, keyless signal — not a trend-prediction engine for your niche.
- Without a local LLM reachable at `FORGE_ENDPOINT`, the script is template-only. That's by design, not a bug: the whole point is that it still works with zero API keys.
- The video is a captioned slideshow, not cinematic editing. Three script templates and three visual styles ship by default — add your own in `templates.py`.
- Font lookup is tested on Linux with Liberation or DejaVu fonts installed; without one of those, captions render in ffmpeg's built-in fallback.
- This produces marketing-style practice copy from a template, not actual proof that any video "brings in customers." No one should take that claim on faith — including the original post's.

## How it fits together

| File | Role |
| --- | --- |
| `config.py` | Env-driven settings: Forge LLM endpoint, output dir, video defaults |
| `scraper.py` | Keyless Hacker News topic scraper with offline fallback |
| `templates.py` | Script template library + visual style library |
| `script_generation.py` | Fills a template with a topic; optional LLM polish pass |
| `forge.py` | Stdlib client for any OpenAI-compatible chat endpoint (Ollama default) |
| `video_creation.py` | Renders captioned clips with ffmpeg and concatenates them |
| `main.py` | CLI that chains scraper → script → video |
| `selftest.py` | End-to-end test: real scraper, real ffmpeg render, canned LLM reply |

Built by Warboy. Free, and it stays free.
