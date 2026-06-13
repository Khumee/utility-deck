#!/usr/bin/env python
import os
import sys
import asyncio
import subprocess

# Auto-install dependencies if missing
try:
    import markdown
except ImportError:
    print("Installing missing dependency: markdown...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
    import markdown

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Installing missing dependency: playwright...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.async_api import async_playwright

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        body {{
            font-family: 'Inter', sans-serif;
            color: #1e293b;
            line-height: 1.6;
            margin: 0;
            padding: 40px;
            background-color: #ffffff;
            font-size: 14px;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: #0f172a;
            font-weight: 700;
            margin-top: 24px;
            margin-bottom: 12px;
            page-break-after: avoid;
        }}

        h1 {{
            font-size: 24px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        h2 {{
            font-size: 18px;
            border-left: 4px solid #0284c7;
            padding-left: 10px;
        }}

        h3 {{
            font-size: 15px;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 16px;
        }}

        a {{
            color: #0284c7;
            text-decoration: none;
        }}

        ul, ol {{
            margin-top: 0;
            margin-bottom: 16px;
            padding-left: 24px;
        }}

        li {{
            margin-bottom: 6px;
        }}

        code {{
            font-family: 'Courier New', Courier, monospace;
            background-color: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 13px;
        }}

        pre {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 16px;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            border-radius: 0;
            font-size: 12px;
        }}

        blockquote {{
            margin: 0 0 16px 0;
            padding: 8px 16px;
            border-left: 4px solid #cbd5e1;
            background-color: #f8fafc;
            color: #475569;
            font-style: italic;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 24px;
            font-size: 13px;
            page-break-inside: auto;
        }}

        tr {{
            page-break-inside: avoid;
            page-break-after: auto;
        }}

        th {{
            background-color: #0f172a;
            color: #ffffff;
            font-weight: 600;
            text-align: left;
            padding: 10px 12px;
            border: 1px solid #1e293b;
        }}

        td {{
            padding: 10px 12px;
            border: 1px solid #e2e8f0;
        }}

        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}

        .footer {{
            margin-top: 40px;
            border-top: 1px solid #e2e8f0;
            padding-top: 10px;
            text-align: center;
            font-size: 11px;
            color: #94a3b8;
        }}

        @media print {{
            body {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    {content}
    <div class="footer">
        Generated document from Markdown
    </div>
</body>
</html>
"""

async def convert_md_to_pdf(md_path, pdf_path):
    if not os.path.exists(md_path):
        print(f"Error: Input file '{md_path}' does not exist.")
        sys.exit(1)
        
    print(f"Reading Markdown from {md_path}...")
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    # Enable common extensions (tables, codehilite, toc, etc.)
    print("Converting Markdown to HTML...")
    html_content = markdown.markdown(
        md_content, 
        extensions=['extra', 'admonition', 'codehilite']
    )
    
    full_html = HTML_TEMPLATE.format(content=html_content)
    
    temp_html_path = md_path + ".temp.html"
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print("Launching Chromium via Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(f"file:///{os.path.abspath(temp_html_path).replace(os.sep, '/')}")
        # Wait for page/fonts rendering
        await page.wait_for_timeout(3000)
        
        print(f"Saving PDF to {pdf_path}...")
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0.4in", "bottom": "0.4in", "left": "0.4in", "right": "0.4in"}
        )
        await page.close()
        await browser.close()
        
    # Clean up temp HTML file
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)
    print("SUCCESS! PDF Generated successfully.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python md_to_pdf.py <input.md> [output.pdf]")
        sys.exit(1)
        
    md_path = sys.argv[1]
    if len(sys.argv) >= 3:
        pdf_path = sys.argv[2]
    else:
        pdf_path = os.path.splitext(md_path)[0] + ".pdf"
        
    asyncio.run(convert_md_to_pdf(md_path, pdf_path))

if __name__ == "__main__":
    main()
