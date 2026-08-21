from playwright.async_api import async_playwright

CBIC_URL = "https://taxinformation.cbic.gov.in/"


async def scrape_cbic_latest():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        await page.goto(
            CBIC_URL,
            wait_until="networkidle",
            timeout=60000
        )

        # Give JS time to populate dynamic content
        await page.wait_for_timeout(3000)

        # Get rendered HTML
        html = await page.content()

        await browser.close()

        return html