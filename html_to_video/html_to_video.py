import argparse
import subprocess
import sys
import os
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error getting duration: {result.stderr}")
        return 0.0
    return float(result.stdout.strip())

def generate_voiceover_script(html_content, language):
    print("Extracting text from HTML for AI script generation...")
    soup = BeautifulSoup(html_content, "html.parser")
    raw_text = soup.get_text(separator="\n", strip=True)
    
    # Trim the text if it's too massive, just to be safe for LLM context limits
    raw_text = raw_text[:30000] 

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set. Please set it to generate scripts.")
        sys.exit(1)

    print(f"Generating {language.upper()} voiceover script using Gemini AI...")
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
You are a professional voiceover script writer. Write an engaging, concise, and highly professional voiceover script summarizing the following content. 
Do not include any stage directions, speaker labels, or filler text. ONLY return the exact spoken words to be synthesized by TTS. 
Output the script completely in {language}. Keep the tone extremely positive and professional.

Content:
{raw_text}
"""
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
        )
    )
    
    script_text = response.text.strip()
    return script_text

def main():
    parser = argparse.ArgumentParser(description="Convert HTML to Video with AI Voiceover")
    parser.add_argument("--html", required=True, help="Path to input HTML file")
    parser.add_argument("--language", default="en", choices=["en", "ur"], help="Language of the voiceover (en or ur)")
    parser.add_argument("--formats", default="mp4,webm", help="Comma separated list of output formats (default: mp4,webm)")
    args = parser.parse_args()

    html_path = Path(args.html).resolve()

    if not html_path.exists():
        print(f"Error: HTML file {html_path} not found.")
        sys.exit(1)

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    script_text = generate_voiceover_script(html_content, "English" if args.language == "en" else "Urdu")
    print(f"\n--- Generated Script ({args.language.upper()}) ---\n{script_text}\n---------------------------\n")

    formats = [f.strip().lower() for f in args.formats.split(',')]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        screenshot_path = tmp_dir / "full_page.png"
        audio_path = tmp_dir / "voiceover.mp3"

        print("1. Synthesizing Audio using edge-tts...")
        # Select appropriate neural voice based on language
        voice = "en-US-AriaNeural" if args.language == "en" else "ur-PK-UzmaNeural"
        
        script_txt_path = tmp_dir / "script.txt"
        with open(script_txt_path, "w", encoding="utf-8") as st:
            st.write(script_text)
            
        tts_cmd = ["edge-tts", "--voice", voice, "-f", str(script_txt_path), "--write-media", str(audio_path)]
        subprocess.run(tts_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

        print("2. Taking full page screenshot with Playwright...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1280, 'height': 720})
            page.goto(f"file:///{html_path}")
            page.wait_for_timeout(2000)
            page.screenshot(path=str(screenshot_path), full_page=True)
            browser.close()

        print("3. Calculating durations...")
        duration = get_audio_duration(audio_path)
        print(f"Audio duration: {duration} seconds")

        print("4. Generating video using FFmpeg...")
        viewport_height = 720
        
        for fmt in formats:
            output_file = html_path.parent / f"{html_path.stem}_video.{fmt}"
            print(f"-> Generating {output_file}...")
            
            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(screenshot_path),
                "-i", str(audio_path),
                "-filter_complex",
                f"[0:v]crop=iw:{viewport_height}:0:'max(0, (ih-{viewport_height})*(t/{duration}))'[v]",
                "-map", "[v]",
                "-map", "1:a",
                "-t", str(duration),
                "-c:v", "libx264" if fmt == "mp4" else "libvpx-vp9",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac" if fmt == "mp4" else "libopus",
                str(output_file)
            ]
            
            subprocess.run(ffmpeg_cmd, check=True)
            print(f"-> Saved {output_file}")
            
    print("All done!")

if __name__ == "__main__":
    main()
