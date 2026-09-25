#!/home/shd/Projects/audio-to-text-ru/bin/python

import argparse
import sys
from pathlib import Path

from faster_whisper import WhisperModel


MODEL_NAME = "avazir/faster-distil-whisper-large-v3-ru"

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".flac",
    ".ogg",
    ".oga",
    ".opus",
    ".webm",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="audio-to-text-ru",
        description="Transcribe Russian audio files using faster-whisper on CUDA.",
    )

    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        metavar="FILE",
        help="audio files or directories to transcribe",
    )

    parser.add_argument(
        "-d",
        "--directory-text-output",
        type=Path,
        help="output directory for .txt files",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="overwrite existing .txt files",
    )

    return parser.parse_args()


def find_audio_files(paths: list[Path]) -> list[Path]:
    result: list[Path] = []

    for path in paths:
        if not path.exists():
            print(
                f"error: file not found: {path}",
                file=sys.stderr,
            )
            continue

        if path.is_dir():
            result.extend(
                file
                for file in sorted(path.iterdir())
                if file.is_file() and file.suffix.lower() in AUDIO_EXTENSIONS
            )

        elif path.is_file():
            if path.suffix.lower() in AUDIO_EXTENSIONS:
                result.append(path)
            else:
                print(
                    f"warning: unsupported audio format: {path}",
                    file=sys.stderr,
                )

    return result


def transcribe(
    model: WhisperModel,
    audio_path: Path,
    output_path: Path,
) -> None:
    print(f"→ {audio_path}")

    segments, _ = model.transcribe(
        str(audio_path),
        language="ru",
        condition_on_previous_text=False,
    )

    text = " ".join(
        segment.text.strip() for segment in segments if segment.text.strip()
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        text + "\n",
        encoding="utf-8",
    )

    print(f"  → {output_path}")


def main() -> int:
    args = parse_args()

    audio_files = find_audio_files(args.files)

    if not audio_files:
        print("No audio files found.", file=sys.stderr)
        return 1

    model = WhisperModel(
        MODEL_NAME,
        device="cuda",
        compute_type="float16",
    )

    failed = False

    for audio_path in audio_files:
        if args.directory_text_output:
            output_path = args.directory_text_output / f"{audio_path.stem}.txt"
        else:
            output_path = audio_path.with_suffix(".txt")

        if output_path.exists() and not args.overwrite:
            print(f"skip: {output_path} already exists")
            continue

        try:
            transcribe(
                model,
                audio_path,
                output_path,
            )
        except Exception as e:
            failed = True
            print(
                f"error: failed to transcribe {audio_path}: {e}",
                file=sys.stderr,
            )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
