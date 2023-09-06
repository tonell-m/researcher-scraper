class Researcher(object):
    """Defines a resaercher object""" 

    def __init__(self, name: str, organisation = None, job_title = None,
                  introduction = None, topics = []) -> None:
        """
        Initialises a Researcher instance with all its props.
        Only name is required upon construction.
        """
        self.name = name
        self.organisation = organisation
        self.job_title = job_title
        self.introduction = introduction
        self.topics = topics

    def is_all_data_filled_in(self) -> bool:
        """Returns true if all values are set for this researcher."""
        return self.organisation is not None and self.job_title is not None and self.introduction is not None and self.topics
    
    def dump(self):
        """Prints all values associated to this researcher in a readable way"""
        print(self.name)
        print(self.organisation)
        print(self.job_title)
        print(self.introduction)
        print(self.topics)