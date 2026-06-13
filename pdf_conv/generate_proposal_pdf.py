import os
import asyncio
import sys

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright is not installed. Please run: pip install playwright && playwright install chromium")
    sys.exit(1)

async def generate_proposal():
    html_path = "D:\\aster\\proposals_and_estimates\\migration_proposal.html"
    pdf_path = "D:\\aster\\proposals_and_estimates\\ASTER_Portaal_Migration_Proposal.pdf"
    
    print("Launching Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"Loading {html_path}...")
        await page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        
        # Wait for google fonts to load
        print("Waiting for page load and fonts...")
        await page.wait_for_timeout(4000)
        
        try:
            print(f"Saving PDF to {pdf_path}...")
            await page.pdf(
                path=pdf_path,
                format="A4",
                print_background=True,
                margin={"top": "0.4in", "bottom": "0.4in", "left": "0.4in", "right": "0.4in"}
            )
        except PermissionError:
            pdf_path_fallback = "D:\\aster\\proposals_and_estimates\\ASTER_Portaal_Migration_Proposal_v2.pdf"
            print(f"Primary file locked. Saving PDF to fallback: {pdf_path_fallback}...")
            await page.pdf(
                path=pdf_path_fallback,
                format="A4",
                print_background=True,
                margin={"top": "0.4in", "bottom": "0.4in", "left": "0.4in", "right": "0.4in"}
            )
        await page.close()
        await browser.close()
    print("PDF Generation complete!")

if __name__ == "__main__":
    asyncio.run(generate_proposal())
