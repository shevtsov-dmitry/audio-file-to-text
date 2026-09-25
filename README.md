# audio to text

## run guide

Create runtime and install packages

```bash
python3 -m venv .
source ./bin/activate
./bin/python -m pip install -U $(cat packages.txt)
```

## Usage

```

```bash
usage: audio-to-text-ru [-h] [-d DIRECTORY_TEXT_OUTPUT] [--overwrite] FILE [FILE ...]

Transcribe Russian audio files using faster-whisper on CUDA.

positional arguments:
  FILE                  audio files or directories to transcribe

options:
  -h, --help            show this help message and exit
  -d, --directory-text-output DIRECTORY_TEXT_OUTPUT
                        output directory for .txt files
  --overwrite           overwrite existing .txt files
```
