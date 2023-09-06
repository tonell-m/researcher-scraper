from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from typing import List
import json

from scrapers.researchgate import ResearchGateDataScraper
from scrapers.ufl import UniversiteLorraineDataScraper
from scrapers.generic import ResearcherDataScraper
from researcher import Researcher

def scrape_researcher(name: str, scrapers: List[ResearcherDataScraper], driver) -> Researcher:
    """Tries to get as much data as possible from the various scraping sources given as parameter"""
    researcher = Researcher(name)

    for scraper in scrapers:
        # Get page contents
        contents = scraper.fetch_contents(name, driver)
        if contents is None:
            continue

        # Try to fill in the various missing information
        if not researcher.organisation:
            researcher.organisation = scraper.get_organisation(contents)
        if not researcher.job_title:
            researcher.job_title = scraper.get_job_title(contents)
        if not researcher.introduction:
            researcher.introduction = scraper.get_introduction(contents)
        if not researcher.topics:
            researcher.topics = scraper.get_topics(contents)
        
        # If all data is filled in, stop looking for more and directly return
        if researcher.is_all_data_filled_in():
            return researcher
    return researcher


def __main__():
    # Use options to spawn a headless chrome instance
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    # Create a Chrome web driver
    driver = webdriver.Chrome(options)

    # Configure stealth options to spoof being a real user and bypass restrictions
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    # Get researchers names from json array
    with open("researchers_list.json") as file:
        names = json.load(file)

    # Instantiate a bunch of scrapers to look for data from different sources
    scrapers: List[ResearcherDataScraper] = [
        UniversiteLorraineDataScraper(),
        ResearchGateDataScraper()
    ]

    for name in names[:20]:
        researcher = scrape_researcher(name, scrapers, driver)
        researcher.dump()
        # Skip some lines for better readability
        print("\n\n")

__main__()