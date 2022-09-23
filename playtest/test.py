from playwright.sync_api import Playwright, sync_playwright, expect
import time
from bs4 import BeautifulSoup


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.momoshop.com.tw/main/Main.jsp
    page.goto("https://www.momoshop.com.tw/main/Main.jsp")

    # Click [placeholder="正官庄"]
    page.locator("[placeholder=\"正官庄\"]").click()

    # Fill [placeholder="正官庄"]
    page.locator("[placeholder=\"正官庄\"]").fill("IPHONE")

    # Click text=iphone 13約5728件商品
    page.locator("text=iphone 13約5728件商品").click()
    page.wait_for_url("https://www.momoshop.com.tw/search/searchShop.jsp?keyword=iphone%2013&searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType")
    time.sleep(5)
    soup = BeautifulSoup(page.content(), 'lxml')
    for li in soup.select('.listArea li'):
        prdname = li.select_one('.prdName').text.strip()
        price = li.select_one('.price > b').text.strip()
        print(prdname, price)

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
