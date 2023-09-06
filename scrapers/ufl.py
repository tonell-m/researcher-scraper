from bs4 import BeautifulSoup
from scrapers.generic import ResearcherDataScraper

class UniversiteLorraineDataScraper(ResearcherDataScraper):
    """`ResearcherDataScraper` implementation for Research Gate"""

    def fetch_contents(self, name: str, driver):
        # Replace whitespace with hyphen to get the URL slug (yeah research gate is easy)
        slugified_name = "-".join(reversed(name.split(" "))).lower()
        # Build URL
        URL = f"http://crem.univ-lorraine.fr/membres/enseignantes-chercheures-titulaires/{slugified_name}"
        # Fetch page contents using web driver
        driver.get(URL)
        # Parse HTML contents using beautiful soup
        contents = BeautifulSoup(driver.page_source, 'html.parser')
        
        if "Page non trouvée" in contents.title.text:
            # For some researchers the page URL is titulaireS and titulaire for some others
            URL = f"http://crem.univ-lorraine.fr/membres/enseignantes-chercheures-titulaire/{slugified_name}"
            driver.get(URL)
            contents = BeautifulSoup(driver.page_source, 'html.parser')
            # If it is not found again it means the researcher is not referenced here
            if "Page non trouvée" in contents.title.text:
                return None

        return contents

    def get_organisation(self, contents: BeautifulSoup):
        """Extracts the researcher's organisation from the page contents"""
        organisation_raw = contents.find_all("div", { "class": "field--name-field-lieu-de-travail" })
        try:
            sub_item = organisation_raw[0].find_all("div", { "class": "field--item" })
            return sub_item[0].text
        except IndexError:
            return None
    
    def get_job_title(self, contents: BeautifulSoup):
        """Extracts the researcher's job title from the page contents"""
        # TODO: Make this dynamic if needed
        return "Professeur·e des universités\nEnseignant·es-chercheur·es titulaires"
    
    def get_introduction(self, contents: BeautifulSoup):
        """Extracts the researcher's information from the page contents"""
        introduction_raw = contents.find_all("div", { "class": "field--name-field-sections-cnu" })
        try:
            sub_item = introduction_raw[0].find_all("div", { "class": "field--item" })
            return sub_item[0].text
        except IndexError:
            return None
    
    def get_topics(self, contents: BeautifulSoup):
        """Extracts the researcher's topics from the page contents"""
        topics_raw = contents.find_all("div", { "class": "field--name-field-axes-thematiques" })
        try:
            sub_item = topics_raw[0].find_all("div", { "class": "field--item" })
            return list(map(lambda li: li.text, sub_item[0].find_all("li")))
        except IndexError:
            return []