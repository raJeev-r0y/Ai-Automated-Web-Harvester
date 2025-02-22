import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Launching chrome browser.....")

    chrome_driver_path = "./chromedriver.exe"  # **Important:** Verify this path
    options = webdriver.ChromeOptions()
    try:  # Try block to handle potential driver issues
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        driver.get(website)
        print("Page loaded....")
        html = driver.page_source
        return html
    except Exception as e:  # Catch potential errors during browser launch/navigation
        print(f"Error during scraping: {e}")
        return None  # Return None to indicate failure
    finally:
        if 'driver' in locals(): # Check if driver was initialized
            driver.quit()
        else:
            print("Driver not initialized, skipping quit")


def extract_body_content(html_content):
    if not html_content:  # Handle cases where scrape_website might return None
        return ""

    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    if not body_content:
        return ""

    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    if not dom_content:
        return []  # Return empty list if dom_content is empty

    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]
