from bs4 import BeautifulSoup
from scrapers.generic import ResearcherDataScraper

class ResearchGateDataScraper(ResearcherDataScraper):
    """`ResearcherDataScraper` implementation for Research Gate"""

    def fetch_contents(self, name: str, driver):
        # Replace whitespace with hyphen to get the URL slug (yeah research gate is easy)
        slugified_name = name.replace(" ", "-")
        # Build URL
        URL = f"https://www.researchgate.net/profile/{slugified_name}"
        # Fetch page contents using web driver
        driver.get(URL)
        # Parse HTML contents using beautiful soup
        return BeautifulSoup(driver.page_source, 'html.parser')

    def get_organisation(self, contents: BeautifulSoup):
        """Extracts the researcher's organisation from the page contents"""
        organisation_raw = contents.find_all("span", { "class": "org" })
        try:
            return organisation_raw[0].text
        except IndexError:
            return None
    
    def get_job_title(self, contents: BeautifulSoup):
        """Extracts the researcher's job title from the page contents"""
        job_title_raw = contents.find_all("div", { "class": "title" })
        try:
            return job_title_raw[0].text
        except IndexError:
            return None
    
    def get_introduction(self, contents: BeautifulSoup):
        """Extracts the researcher's information from the page contents"""
        introduction_raw = contents.find_all("span", { "class": "Linkify" })
        try:
            return introduction_raw[0].text
        except IndexError:
            return None
    
    def get_topics(self, contents: BeautifulSoup):
        """Extracts the researcher's topics from the page contents"""
        skills_raw = contents.find_all("div", { "class": "js-target-skills" })
        try:
            return list(map(lambda link: link.text, skills_raw[0].find_all("a")))
        except IndexError:
            return []