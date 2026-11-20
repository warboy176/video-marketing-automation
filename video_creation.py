"""Renders a script into a captioned slideshow video with ffmpeg.

No stock footage, no text-to-speech: each line gets a timed caption on a
solid-color background, and the clips are concatenated into one silent mp4.
Text is written to a temp file and passed to ffmpeg's drawtext via
`textfile=`, never interpolated into the filter string, so a script line
full of colons or quotes can't break (or inject into) the ffmpeg command.
"""
import os
import shutil
import subprocess
import tempfile
import textwrap

from config import FPS, SECONDS_PER_LINE, VIDEO_HEIGHT, VIDEO_WIDTH
from templates import VIDEO_STYLES

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]


def _find_font():
    for candidate in FONT_CANDIDATES:
        if os.path.exists(candidate):
            return candidate
    return None


def _wrap(text, width=28):
    return "\n".join(textwrap.wrap(text, width=width)) or " "


def render_video(
    lines,
    output_path,
    style="default",
    width=None,
    height=None,
    fps=None,
    seconds_per_line=None,
):
    """Render `lines` into a captioned mp4 at `output_path`. Returns the path."""
    if not lines:
        raise ValueError("render_video needs at least one line")
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is not installed or not on PATH")

    style_cfg = VIDEO_STYLES.get(style, VIDEO_STYLES["default"])
    w = width or VIDEO_WIDTH
    h = height or VIDEO_HEIGHT
    f = fps or FPS
    dur = seconds_per_line or SECONDS_PER_LINE
    font = _find_font()

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        segment_paths = []
        for i, line in enumerate(lines):
            text_path = os.path.join(tmp, f"line_{i}.txt")
            with open(text_path, "w") as fh:
                fh.write(_wrap(line))

            drawtext = (
                f"drawtext=textfile={text_path}:fontcolor={style_cfg['text_color']}"
                f":fontsize=56:line_spacing=12:x=(w-text_w)/2:y=(h-text_h)/2"
            )
            if font:
                drawtext += f":fontfile={font}"

            seg_path = os.path.join(tmp, f"seg_{i}.mp4")
            cmd = [
                "ffmpeg", "-y", "-loglevel", "error",
                "-f", "lavfi", "-i", f"color=c={style_cfg['bg_color']}:s={w}x{h}:d={dur}:r={f}",
                "-vf", drawtext,
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                seg_path,
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            segment_paths.append(seg_path)

        concat_list = os.path.join(tmp, "concat.txt")
        with open(concat_list, "w") as fh:
            for p in segment_paths:
                fh.write(f"file '{p}'\n")

        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", concat_list,
            "-c", "copy",
            output_path,
        ]
        subprocess.run(cmd, check=True, capture_output=True)

    return output_path
