"""Assemble an assistant-authored storyboard with narration and subtitles."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FPS = 30
WIDTH, HEIGHT = 1920, 1080


def run(command: list[str], log: Path) -> None:
    with log.open("w", encoding="utf-8") as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"FFmpeg não concluiu a etapa; consulte {log.name}.")


def to_ass_time(value: str) -> str:
    return value.replace(",", ".")[:-1]


def make_ass(srt: str) -> str:
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,40,&H00F8F4ED,&H00F8F4ED,&H00221B12,&HAA221B12,0,0,0,0,100,100,0,0,3,2,0,2,100,100,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    entries = []
    for block in re.split(r"\n\s*\n", srt.strip()):
        lines = block.splitlines()
        if len(lines) < 3:
            raise ValueError("Legenda SRT inválida.")
        start, end = lines[1].split(" --> ")
        # Literal braces cannot inject ASS override instructions.
        spoken = r"\N".join(lines[2:]).replace("{", "｛").replace("}", "｝")
        entries.append(f"Dialogue: 0,{to_ass_time(start)},{to_ass_time(end)},Default,,0,0,0,,{spoken}")
    return header + "\n".join(entries) + "\n"


def render_shot(index: int, shot: dict, episode: Path, work: Path) -> Path:
    asset = (episode / shot["asset"]).resolve()
    if not asset.is_relative_to(episode.resolve()) or not asset.is_file():
        raise ValueError("Imagem ausente ou fora da pasta do episódio.")
    frames = round(float(shot["duration_seconds"]) * FPS)
    if frames <= 0:
        raise ValueError("Duração de cena inválida.")
    output = work / f"clip-{index:03d}.mp4"
    filters = [f"scale={WIDTH}:{HEIGHT}", "setsar=1"]
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    if shot.get("motion", False):
        command += ["-i", str(asset)]
        filters.append(f"zoompan=z='1+0.035*on/{frames}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS}")
    else:
        command += ["-loop", "1", "-framerate", str(FPS), "-i", str(asset)]
    for field, y, size in (("caption", 155, 66), ("label", 910, 25)):
        if value := shot.get(field):
            textfile = work / f"clip-{index:03d}-{field}.txt"
            textfile.write_text(value, encoding="utf-8")
            filters.append(f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:textfile='{textfile}':fontcolor=0xfff3df:fontsize={size}:x=90:y={y}:box=1:boxcolor=0x091b2b@0.75:boxborderw=16")
    filters += ["format=yuv420p"]
    command += ["-vf", ",".join(filters), "-frames:v", str(frames), "-an",
                "-c:v", "libx264", "-preset", "fast", "-crf", "24", "-threads", "2",
                "-r", str(FPS), "-movflags", "+faststart", str(output)]
    run(command, work / f"clip-{index:03d}.log")
    print(f"Cena {index + 1:02d} concluída.", flush=True)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    episode, work = args.episode.resolve(), args.work_dir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    storyboard = json.loads((episode / "storyboard.json").read_text(encoding="utf-8"))
    duration = float(storyboard["duration_seconds"])
    shots = storyboard["shots"]
    if not shots or abs(sum(round(s["duration_seconds"] * FPS) for s in shots) / FPS - duration) > 1 / FPS:
        raise ValueError("As cenas não cobrem a duração declarada.")
    narration_report = json.loads((work / "narracao.json").read_text(encoding="utf-8"))
    if narration_report["duration_seconds"] > duration:
        raise ValueError("A narração ultrapassa o fim do vídeo. Ajuste o roteiro ou o ritmo da voz.")
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 3))) as pool:
        clips = list(pool.map(lambda pair: render_shot(pair[0], pair[1], episode, work), enumerate(shots)))
    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{clip.name}'\n" for clip in clips), encoding="utf-8")
    silent = work / "silent.mp4"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "1",
         "-i", str(concat), "-c", "copy", str(silent)], work / "concat.log")
    ass = work / "legendas.ass"
    ass.write_text(make_ass((work / "legendas.srt").read_text(encoding="utf-8")), encoding="utf-8")
    final_tmp = episode / "video.partial.mp4"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-i", str(silent), "-i", str(work / "narracao.mp3"),
         "-vf", f"ass='{ass}',fade=t=out:st={duration-1}:d=1",
         "-af", f"loudnorm=I=-16:TP=-1.5:LRA=9,apad,afade=t=out:st={duration-0.7}:d=0.7",
         "-t", str(duration), "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-threads", "2",
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(final_tmp)], work / "final.log")
    final_tmp.replace(episode / "video.mp4")
    shutil.copyfile(work / "legendas.srt", episode / "legendas.srt")
    shutil.copyfile(work / "narracao.json", episode / "narracao.json")
    print(f"Vídeo montado: {duration:.2f} s, {len(shots)} cenas, 1920 × 1080.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
