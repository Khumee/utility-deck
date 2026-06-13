import os
import sys
import asyncio
import argparse

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

async def capture_image(html_path, image_path, width, height, scale, selector, wait_ms):
    print(f"Loading HTML: {os.path.basename(html_path)}")
    abs_url = f"file:///{os.path.abspath(html_path).replace(os.sep, '/')}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=scale
        )
        page = await context.new_page()
        await page.goto(abs_url)
        
        if wait_ms > 0:
            print(f"Waiting {wait_ms}ms for assets/fonts to load...")
            await page.wait_for_timeout(wait_ms)
            
        print(f"Capturing screenshot to: {os.path.basename(image_path)}...")
        if selector:
            # Screenshot specific element
            element = page.locator(selector)
            if await element.count() > 0:
                await element.screenshot(path=image_path)
            else:
                print(f"Warning: Selector '{selector}' not found. Capturing full viewport.")
                await page.screenshot(path=image_path)
        else:
            # Screenshot full viewport
            await page.screenshot(path=image_path)
            
        print("SUCCESS! Image saved.")
        await browser.close()

async def async_main():
    parser = argparse.ArgumentParser(
        description="General-purpose HTML to high-resolution Image converter using Playwright."
    )
    parser.add_argument("-i", "--input", required=True, help="Input HTML file path.")
    parser.add_argument("-o", "--output", help="Output image file path (default: same name with .png extension).")
    parser.add_argument("-w", "--width", type=int, default=500, help="Viewport width (default: 500).")
    parser.add_argument("-g", "--height", type=int, default=750, help="Viewport height (default: 750).")
    parser.add_argument("-s", "--scale", type=int, default=3, help="Device scale factor / resolution scale (default: 3).")
    parser.add_argument("-e", "--element", default=".whatsapp-flyer", help="CSS selector of element to screenshot (default: .whatsapp-flyer). Pass empty string for full page.")
    parser.add_argument("-t", "--wait", type=int, default=2000, help="Wait time in milliseconds for fonts (default: 2000ms).")
    
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        print(f"Error: Input path '{input_path}' does not exist.")
        sys.exit(1)

    output_path = args.output
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + ".png"
    output_path = os.path.abspath(output_path)

    # Use element selector unless explicitly cleared
    selector = args.element if args.element else None

    try:
        await capture_image(
            input_path, 
            output_path, 
            args.width, 
            args.height, 
            args.scale, 
            selector, 
            args.wait
        )
    except Exception as e:
        print(f"Error converting HTML to image: {e}")
        sys.exit(1)

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
