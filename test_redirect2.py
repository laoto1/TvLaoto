from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    response = page.goto("https://vtvgo.vn/channel/vtv1-1,1.html")
    print("Status:", response.status)
    print("Final URL:", page.url)
    
    browser.close()
