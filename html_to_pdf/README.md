# HTML to PDF Converter

Converts HTML files (or directories containing HTML files) to print-ready A4 PDFs using Playwright.

## Setup:
```bash
pip install playwright
playwright install chromium
```

## Usage:
```bash
# Convert a single HTML file
python html_to_pdf.py --input "document.html" --output "output.pdf"

# Convert a folder of HTML files
python html_to_pdf.py --input "C:\path\to\html_folder" --wait 3500
```
* Use `-w` or `--wait` to specify the delay (in milliseconds) to wait for fonts or web-assets to load before rendering.
