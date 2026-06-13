import os
import sys
import argparse
import re
import mimetypes
import time

try:
    from google import genai
    from google.genai import errors
    from google.genai import types
except ImportError:
    print("Installing required package 'google-genai'...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai"])
        from google import genai
        from google.genai import errors
        from google.genai import types
    except Exception as err:
        print(f"Error: Could not install 'google-genai' automatically: {err}")
        print("Please install it manually using: pip install google-genai")
        sys.exit(1)

def extract_html(text):
    """Strips markdown blocks like ```html ... ``` from the response text."""
    # Look for ```html ... ```
    match = re.search(r'```html\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Look for generic ``` ... ```
    match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()

def main():
    parser = argparse.ArgumentParser(
        description="Convert flyer, layout or design image to semantic HTML/CSS using Gemini API."
    )
    parser.add_argument("-f", "--file", required=True, help="Path to the input image file (.jpeg, .jpg, .png, etc.)")
    parser.add_argument("-k", "--key", help="Gemini API Key (default: GEMINI_API_KEY environment variable)")
    parser.add_argument("-m", "--model", default="gemini-2.5-flash", help="Gemini model to use (default: gemini-2.5-flash)")
    parser.add_argument("-o", "--output", help="Path to save output HTML file (default: same name/path as image with .html extension)")
    
    args = parser.parse_args()

    # Get API Key
    api_key = args.key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Gemini API Key is required.")
        print("Please set the GEMINI_API_KEY environment variable or pass the key using --key.")
        sys.exit(1)

    # Validate file path
    image_path = os.path.abspath(args.file)
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at '{image_path}'")
        sys.exit(1)

    # Detect mime type
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith("image/"):
        # Default fallback
        mime_type = "image/jpeg"

    print(f"File: {os.path.basename(image_path)} ({os.path.getsize(image_path)/(1024):.2f} KB) - Mime: {mime_type}")
    print(f"Model: {args.model}")

    # Initialize client
    client = genai.Client(api_key=api_key)

    try:
        # Read image bytes
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # Request Image-to-HTML Conversion
        prompt = (
            "Analyze the layout, design, structure, colors, typography, and text of the provided image.\n"
            "Generate a highly professional, modern, fully responsive, and beautifully designed single-file HTML webpage.\n"
            "Requirements:\n"
            "1. Output valid HTML5 with semantic elements.\n"
            "2. All styles must be written inside a <style> tag in the <head>. Do NOT use external CSS frameworks like Tailwind or Bootstrap unless asked, use clean Vanilla CSS. Use modern layout methodologies like Flexbox and CSS Grid.\n"
            "3. The design should look extremely polished and premium, mirroring the style, theme, color scheme, and content of the flyer/image as closely as possible.\n"
            "4. Transcribe all text from the image accurately. If the text is in Urdu or Arabic, make sure to use correct direction attributes (dir=\"rtl\") and nice fonts (e.g. Google Fonts like Jameel Noori Nastaliq, Noto Naskh Arabic, or Noto Nastaliq Urdu) to render it elegantly.\n"
            "5. Structure the page logically (e.g. Header/Hero, main content, details/features section, call to action / donation section, footer).\n"
            "6. Provide modern micro-animations/hover-effects on interactive elements (like buttons).\n"
            "7. Return ONLY the HTML code. Do not wrap it with markdown text or write introductory or explanatory remarks outside the HTML code."
        )

        max_retries = 3
        retry_delay = 5
        response = None

        for attempt in range(1, max_retries + 1):
            print(f"Converting image to HTML via Gemini inline bytes (Attempt {attempt}/{max_retries})...")
            try:
                response = client.models.generate_content(
                    model=args.model,
                    contents=[
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=mime_type
                        ),
                        prompt
                    ]
                )
                # If successful, break retry loop
                break
            except Exception as conn_err:
                print(f"Error on attempt {attempt}: {conn_err}")
                if attempt < max_retries:
                    print(f"Waiting {retry_delay} seconds before retrying...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise conn_err

        if not response:
            print("Error: Did not receive response from Gemini API.")
            sys.exit(1)

        # Extract HTML & Output
        raw_text = response.text
        html_content = extract_html(raw_text)

        # Resolve output path
        output_path = args.output or os.path.splitext(image_path)[0] + ".html"
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(html_content)
        print(f"Success! HTML page saved to: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"\nAn error occurred during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
