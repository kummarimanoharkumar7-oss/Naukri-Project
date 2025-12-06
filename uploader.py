import asyncio
import os
from dotenv import load_dotenv
from pyppeteer import launch

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CV_PATH = os.getenv("CV_PATH", "/app/resume.pdf")  # FIXED PATH

async def login(page):
    await page.goto("https://www.naukri.com/", {"waitUntil": "networkidle2"})
    await page.click("#login_Layer")

    await page.type("input[placeholder='Enter your active Email ID / Username']", EMAIL)
    await page.type("input[placeholder='Enter your password']", PASSWORD)

    await page.click("button[type='submit']")
    await page.waitForNavigation()

    print("Logged in.")

async def go_to_profile(page):
    await page.goto("https://www.naukri.com/mnjuser/profile", {"waitUntil": "networkidle0"})
    await asyncio.sleep(2)
    print("On Profile page.")

async def upload_resume(page):
    try:
        file_input = await page.querySelector("input[type=file]")
        await file_input.uploadFile(CV_PATH)
        print("Resume Uploaded.")
    except Exception as e:
        print("Upload failed:", e)

async def update_headline(page):
    try:
        await page.click("span.edit.icon")
        await page.waitForSelector("#resumeHeadlineTxt")
        await page.evaluate("""() => {
            document.querySelector('#resumeHeadlineTxt').value = 'Experienced Data Scientist';
        }""")

        await page.click("button[type=submit]")
        print("Headline Updated.")
    except Exception:
        print("Headline update skipped.")

async def run_uploader():
    browser = await launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )

    page = await browser.newPage()

    await login(page)
    await go_to_profile(page)

    upload_timer = 0

    while True:
        try:
            await go_to_profile(page)
            await asyncio.sleep(2)

            # Resume upload every 30 min
            if upload_timer % 6 == 0:
                await upload_resume(page)
                await update_headline(page)
                print("Updated successfully!")

            upload_timer += 1
            await asyncio.sleep(300)  # refresh every 5 min

        except Exception as e:
            print("Error in loop:", e)
            await asyncio.sleep(10)
