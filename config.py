import os

# Optional LLM polishing step. Points at a local Ollama server by default so the
# whole pipeline works with zero API keys and zero cost. Only used if main.py is
# run with --use-forge; everything else works fine with this unreachable.
FORGE_ENDPOINT = os.getenv("FORGE_ENDPOINT", "http://localhost:11434/v1")
FORGE_MODEL = os.getenv("FORGE_MODEL", "llama3.2")
FORGE_API_KEY = os.getenv("FORGE_API_KEY", "ollama")

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

# Default render settings for a vertical short-form video.
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30
SECONDS_PER_LINE = 3.0
