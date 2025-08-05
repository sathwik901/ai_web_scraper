import os
from selenium.webdriver import Remote, ChromeOptions
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Connecting to Scraping Browser...")

    selenium_url = "https://brd-customer-hl_7274484a-zone-scraping_browser1:80hh8yizz5hn@brd.superproxy.io:9515"

    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Connecting to the remote browser with embedded auth
    driver = Remote(
        command_executor=selenium_url,
        options=options
    )

    print("Navigating to site...")
    driver.get(website)

    print("Waiting captcha to solve...")
    try:
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
    except Exception as e:
        print("Captcha solve error:", e)

    print("Scraping page content...")
    html = driver.page_source
    driver.quit()
    return html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
