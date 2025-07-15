from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_website_data(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # SEO meta tags
    seo_meta = {
        "title": soup.title.string if soup.title else "",
        "description": "",
        "keywords": [],
    }

    for tag in soup.find_all("meta"):
        if tag.get("name") == "description":
            seo_meta["description"] = tag.get("content", "")
        if tag.get("name") == "keywords":
            seo_meta["keywords"] = tag.get("content", "").split(",")

    # Cookies
    cookies = driver.get_cookies()

    # DataLayers
    datalayers = driver.execute_script("return window.dataLayer || []")

    driver.quit()

    return {
        "seo_meta": seo_meta,
        "cookies": cookies,
        "datalayers": datalayers,
        "keywords": seo_meta["keywords"],
    }
