# Audio Transcriber

Transcribes audio files (like `.mp3`, `.ogg`, `.wav`) to text using Google's Gemini API (via the new `google-genai` SDK supporting `AQ.` key formats).

## Setup:
```bash
pip install google-genai
```
Configure your API key in your environment variables:
* **Windows (PowerShell)**: `[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your_key", "User")`
* **Linux/macOS**: `export GEMINI_API_KEY="your_key"`

## Usage:
```bash
python audio_transcriber.py --file "path/to/audio.ogg" --language "Urdu"
```
* Use `-f` or `--file` to specify the audio path.
* Use `-o` or `--output` to customize the output text file destination.
* Use `-m` or `--model` to change the Gemini model (default is `gemini-2.5-flash`).
