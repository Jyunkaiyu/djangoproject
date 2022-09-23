import time
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://24h.pchome.com.tw/
    page.goto("https://24h.pchome.com.tw/")

    # Click [placeholder="輸入你想找的商品"]
    page.locator("[placeholder=\"輸入你想找的商品\"]").click()

    # Fill [placeholder="輸入你想找的商品"]
    page.locator("[placeholder=\"輸入你想找的商品\"]").fill("iphone")

    # Click li[role="option"]:has-text("iphone 14 promax")
    page.locator("li[role=\"option\"]:has-text(\"iphone 14 promax\")").click()
    page.wait_for_url("https://ecshweb.pchome.com.tw/search/v3.3/?q=iphone%2014%20promax")
    time.sleep(5)
    page.screenshot(path='pchome.jpg', full_page = True)
    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
