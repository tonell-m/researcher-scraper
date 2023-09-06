from bs4 import BeautifulSoup

class ResearcherDataScraper():
    """Defines a set of methods that scrape all required data for a researcher from a web page"""

    def fetch_contents(self, name: str, driver):
        """Fetches the page contents from the researcher's name"""
        pass

    def get_organisation(self, contents: BeautifulSoup):
        """Extracts the researcher's organisation from the page contents"""
        pass
    
    def get_job_title(self, contents: BeautifulSoup):
        """Extracts the researcher's job title from the page contents"""
        pass
    
    def get_introduction(self, contents: BeautifulSoup):
        """Extracts the researcher's information from the page contents"""
        pass
    
    def get_topics(self, contents: BeautifulSoup):
        """Extracts the researcher's topics from the page contents"""
        pass
