import os
import asyncio
import sys
import shutil

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright is not installed. Please run:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)

async def render_to_pdf(page, html_path, pdf_path, label):
    print(f"[{label}] Loading HTML...")
    await page.goto(f"file:///{html_path.replace(os.sep, '/')}")
    print(f"[{label}] Waiting for fonts...")
    await page.wait_for_timeout(3500)
    print(f"[{label}] Rendering PDF...")
    await page.pdf(
        path=pdf_path,
        format="A4",
        print_background=True,
        margin={"top": "0px", "bottom": "0px", "left": "0px", "right": "0px"}
    )
    print(f"[{label}] SUCCESS! PDF saved.")
    print("-" * 50)

async def generate_all():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Use glob to find the Urdu-named files
    import glob

    all_html = glob.glob(os.path.join(current_dir, "*.html"))
    brochure_html = None
    flyer_html    = None

    for f in all_html:
        name = os.path.basename(f)
        # Detect by file size: brochure is ~39KB, flyer is ~19KB
        size = os.path.getsize(f)
        if "\u0628\u0631\u0648\u0634\u0631" in name:   # بروشر
            brochure_html = f
        elif "\u0641\u0644\u0627\u0626\u0631" in name:  # فلائر
            flyer_html = f

    if not brochure_html:
        print("Brochure HTML not found!")
    if not flyer_html:
        print("Flyer HTML not found!")

    brochure_pdf = os.path.join(current_dir, "\u0634\u0634\u0645\u0627\u06c1\u06cc \u062a\u0631\u0628\u06cc\u062a\u06cc \u067e\u0631\u0648\u06af\u0631\u0627\u0645 \u0628\u0631\u0648\u0634\u0631.pdf")
    flyer_pdf    = os.path.join(current_dir, "\u0634\u0634\u0645\u0627\u06c1\u06cc \u062a\u0631\u0628\u06cc\u062a\u06cc \u067e\u0631\u0648\u06af\u0631\u0627\u0645 \u0641\u0644\u0627\u0626\u0631.pdf")

    print("Launching headless Chromium...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        if brochure_html:
            page = await browser.new_page()
            await render_to_pdf(page, brochure_html, brochure_pdf, "Brochure")
            await page.close()

        if flyer_html:
            page = await browser.new_page()
            await render_to_pdf(page, flyer_html, flyer_pdf, "Flyer")
            await page.close()

        await browser.close()

    print("All done!")

if __name__ == "__main__":
    asyncio.run(generate_all())
