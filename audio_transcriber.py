import os
import sys
import time
import argparse

try:
    from google import genai
    from google.genai import errors
except ImportError:
    print("Installing required package 'google-genai'...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai"])
        from google import genai
        from google.genai import errors
    except Exception as err:
        print(f"Error: Could not install 'google-genai' automatically: {err}")
        print("Please install it manually using: pip install google-genai")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="General-purpose Audio Transcription Utility using Google Gemini API (AI Studio Free Tier)."
    )
    parser.add_argument("-f", "--file", required=True, help="Path to the input audio file (.mp3, .ogg, .wav, etc.)")
    parser.add_argument("-k", "--key", help="Gemini API Key (default: GEMINI_API_KEY environment variable)")
    parser.add_argument("-m", "--model", default="gemini-2.5-flash", help="Gemini model to use (default: gemini-2.5-flash)")
    parser.add_argument("-o", "--output", help="Path to save output transcription (default: same name as audio with .txt extension)")
    parser.add_argument("-l", "--language", default="Urdu", help="Language spoken in the audio file (default: Urdu)")
    
    args = parser.parse_args()

    # Get API Key
    api_key = args.key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Gemini API Key is required.")
        print("Please set the GEMINI_API_KEY environment variable or pass the key using --key.")
        sys.exit(1)

    # Validate file path
    audio_path = os.path.abspath(args.file)
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at '{audio_path}'")
        sys.exit(1)

    print(f"File: {os.path.basename(audio_path)} ({os.path.getsize(audio_path)/(1024*1024):.2f} MB)")
    print(f"Model: {args.model}")
    print(f"Language: {args.language}")

    # Initialize client
    client = genai.Client(api_key=api_key)

    try:
        # 1. Upload the file
        print("Uploading file to Gemini File API...")
        uploaded_file = client.files.upload(file=audio_path)
        print(f"Upload complete. File reference: {uploaded_file.name}")

        # 2. Wait for processing
        print("Processing file on server...", end="", flush=True)
        while True:
            file_info = client.files.get(name=uploaded_file.name)
            if file_info.state.name == "ACTIVE":
                print(" [ACTIVE]")
                break
            elif file_info.state.name == "FAILED":
                print(" [FAILED]")
                print("Error: File processing failed on Gemini server.")
                sys.exit(1)
            else:
                print(".", end="", flush=True)
                time.sleep(2.5)

        # 3. Generate Transcription
        print(f"Transcribing audio using {args.model}...")
        prompt = (
            f"This is a {args.language} audio file. Please transcribe the audio accurately word-for-word. "
            f"Output ONLY the text transcript. Do not add any introduction, explanations, metadata, or extra notes."
        )

        response = client.models.generate_content(
            model=args.model,
            contents=[uploaded_file, prompt]
        )

        # 4. Clean up the file from server
        print("Cleaning up file from server...")
        try:
            client.files.delete(name=uploaded_file.name)
        except Exception as delete_err:
            print(f"Warning: Could not delete remote file: {delete_err}")

        # 5. Output Result
        transcript = response.text.strip()
        print("\n--- Transcription Result ---")
        print(transcript)
        print("----------------------------\n")

        # Save to output file
        output_path = args.output or os.path.splitext(audio_path)[0] + ".txt"
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(transcript)
        print(f"Success! Transcription saved to: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"\nAn error occurred during transcription: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
