import random
import time
from playwright.sync_api import sync_playwright


def run(playwright):
    browser = playwright.firefox.launch(headless=False)

    def random_delay(min_seconds=1, max_seconds=3):
        """Generate a random delay to mimic human behavior."""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def collect_paragraphs_from_page(page, href):
        print(f"Processing page: {href}")

        # Wait for elements to load on the page
        page.wait_for_selector("div.row")

        paragraph_counter = 0
        for row in page.query_selector_all("div.row"):
            message_content = row.query_selector("div.message-col > div.message-content > p")
            if message_content and "sarcasm" in message_content.text_content().lower():
                paragraph_counter += 1
                print(f"Paragraph {paragraph_counter}: {message_content.text_content()}")
                random_delay()

        if paragraph_counter == 0:
            print(f"Nothing found on the page: {href}")

    page = browser.new_page()
    page.goto("https://wrongplanet.net/search-results/?cx=partner-pub-8703422890298959%3Aq5of6baj6hj&cof=FORID%3A10&ie=ISO-8859-1&q=%22sarcasm%22+%22autism%22&sa=Submit")
    random_delay()

    # Check if iframe exists and wait for it to load
    if page.wait_for_selector("iframe[name='googleSearchFrame']"):
        iframe = page.frame(name="googleSearchFrame")
        iframe.wait_for_selector("a.gs-title")
        random_delay()

        # Pagination loop
        current_page = 1
        while True:
            print(f"Starting Page {current_page}")
            unique_hrefs = set(link.get_attribute("href") for link in iframe.query_selector_all("a.gs-title"))

            for href in unique_hrefs:
                if href is None or not href.startswith('http'):
                    continue

                # Open a new tab for each link
                new_tab = browser.new_page()
                try:
                    new_tab.goto(href, timeout=60000)  # Increase timeout to 60 seconds
                    collect_paragraphs_from_page(new_tab, href)
                except Exception as e:
                    print(f"Error while processing page: {href}")
                    print(e)
                finally:
                    new_tab.close()

            print(f"Page {current_page} finished")
            current_page += 1
            pagination_buttons = iframe.query_selector_all(".gsc-cursor-page")
            if current_page > len(pagination_buttons):
                print("No more pages to process")
                break  # Break if there are no more pages

            pagination_buttons[current_page - 1].click()
            random_delay()
    else:
        print("Iframe not found or not loaded properly")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
