import os
import sys
import asyncio
import argparse

# Reconfigure stdout/stderr to use UTF-8 for clean console output of unicode/Urdu
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright is not installed.")
    print("Installing Playwright...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        from playwright.async_api import async_playwright
    except Exception as err:
        print(f"Error: Could not install Playwright automatically: {err}")
        print("Please run manually:")
        print("  pip install playwright")
        print("  playwright install chromium")
        sys.exit(1)

async def render_to_pdf(page, html_path, pdf_path, wait_ms):
    print(f"Loading HTML: {os.path.basename(html_path)}")
    # Convert file path to local URL format
    abs_url = f"file:///{os.path.abspath(html_path).replace(os.sep, '/')}"
    await page.goto(abs_url)
    
    if wait_ms > 0:
        print(f"Waiting {wait_ms}ms for fonts/assets to load...")
        await page.wait_for_timeout(wait_ms)
        
    print(f"Rendering PDF to: {os.path.basename(pdf_path)}...")
    await page.pdf(
        path=pdf_path,
        format="A4",
        print_background=True,
        margin={"top": "0px", "bottom": "0px", "left": "0px", "right": "0px"}
    )
    print("SUCCESS! PDF saved.")
    print("-" * 50)

async def main():
    parser = argparse.ArgumentParser(
        description="General-purpose HTML to A4 Print PDF Converter using Playwright."
    )
    parser.add_argument("-i", "--input", required=True, help="Input HTML file path or folder path containing HTML files.")
    parser.add_argument("-o", "--output", help="Output PDF file path (or output directory if input is a folder).")
    parser.add_argument("-w", "--wait", type=int, default=3500, help="Wait time in milliseconds for rendering (default: 3500ms).")
    
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        print(f"Error: Input path '{input_path}' does not exist.")
        sys.exit(1)

    # Resolve HTML files to compile
    html_files = []
    if os.path.isdir(input_path):
        for f in os.listdir(input_path):
            if f.lower().endswith(".html"):
                html_files.append(os.path.join(input_path, f))
        if not html_files:
            print(f"Error: No .html files found in directory '{input_path}'")
            sys.exit(1)
    else:
        if not input_path.lower().endswith(".html"):
            print("Error: Input file must have .html extension.")
            sys.exit(1)
        html_files.append(input_path)

    # Resolve output path
    output_path = args.output
    if output_path:
        output_path = os.path.abspath(output_path)

    print(f"Found {len(html_files)} HTML file(s) to convert.")
    
    print("Launching Playwright headless Chromium...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for html_file in html_files:
            # Determine output PDF path for each file
            if os.path.isdir(input_path):
                # Input is a folder, output should be inside output folder or same folder
                out_dir = output_path if output_path and os.path.isdir(output_path) else input_path
                pdf_name = os.path.splitext(os.path.basename(html_file))[0] + ".pdf"
                pdf_file = os.path.join(out_dir, pdf_name)
            else:
                # Input is a single file
                if output_path:
                    # Output path can be a directory or a specific file name
                    if os.path.isdir(output_path) or output_path.endswith(os.sep):
                        pdf_name = os.path.splitext(os.path.basename(html_file))[0] + ".pdf"
                        pdf_file = os.path.join(output_path, pdf_name)
                    else:
                        pdf_file = output_path
                else:
                    pdf_file = os.path.splitext(html_file)[0] + ".pdf"

            page = await browser.new_page()
            try:
                await render_to_pdf(page, html_file, pdf_file, args.wait)
            except Exception as e:
                print(f"Error converting '{os.path.basename(html_file)}': {e}")
            finally:
                await page.close()

        await browser.close()
    print("All conversions completed.")

if __name__ == "__main__":
    asyncio.run(main())
