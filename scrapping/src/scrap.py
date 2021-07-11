from enum import Enum
from typing import List
from bs4 import BeautifulSoup
import pandas as pd
import requests

class StackTab(str, Enum):
    """
        Enum of all question tabs for Stackoverflow. This ensures that the user doesnt have to provide URL for scrapping.
    """
    NEW = "https://stackoverflow.com/questions?tab=Newest&pagesize=50"
    ACTIVE = "https://stackoverflow.com/questions?tab=Active&pagesize=50"
    BOUNTIFIED = "https://stackoverflow.com/questions?tab=Bounties&pagesize=50"
    UNANSWERED = "https://stackoverflow.com/questions?tab=Unanswered&pagesize=50"
    FREQUENT = "https://stackoverflow.com/questions?tab=Frequent&pagesize=50"
    VOTES = "https://stackoverflow.com/questions?tab=Votes&pagesize=50"

class ScrapStackOverflow:
    """
        A class used to scrap StackOverflow website for questions
        The filter for scrapping is Recent Activity
        ...

        Attributes
        ----------
        scrapped_url : str
            the url that is scrapped
        name : str
            the name of the animal
        sound : str
            the sound that the animal makes
        num_legs : int
            the number of legs the animal has (default 4)

        Methods
        -------
        says(sound=None)
            Prints the animals name and what sound it makes
    """

    def __init__(self, tab: Enum = StackTab.ACTIVE) -> None:
        """
            Parameters
            ----------
            tab : Enum
                The Enum of the question tab to be scrapped. Default is StackTab.ACTIVE

            Raises
            ------
            TypeError
                if tab isnt a valid member of StackTab Enum, Type Error is raised.
            
        """
        if not isinstance(tab, StackTab):
            raise TypeError("tab must be an instance of StackTab Enum")

        self.__url = tab.value
        self.__items = []

    @property
    def scrapped_url(self) -> str:
        """
            Returns the scrapped url
        """
        return self.__url

    def scrap(self, num_of_samples:int = 10) -> pd.DataFrame:
        """Scraps the requested .

        Scraps the url and returns a dataframe of size num_of_samples

        Parameters
        ----------
        num_of_samples : int
            The number of samples to be collected from the url. Default is 10

        Raises
        ------
        TypeError
            If num of samples isnt int, TypeError is raised.

        Returns
        -------
        list
            a Dataframe of scrapped items
        """
        if not isinstance(num_of_samples, int):
            raise TypeError("integer expected for num_of_samples")

        page_count = round(num_of_samples/50) if round(num_of_samples % 100) == 0 else round(num_of_samples/ 100) + 1
        self.__combinedProcessing(page_count, num_of_samples)

        return pd.DataFrame(self.__items)

    def  __combinedProcessing(self, page_count, num_of_samples) -> None:
        """
            Run the processing
        """
        for num in range(0, page_count):
            url = f"{self.__url}&page={num}"
            page_content = self.__get_page_content(url)
            self.__scrap_content(page_content[1], num_of_samples)
            

    def __get_page_content(self, url: str) -> tuple:
        """
            Scraps a html content of the url

            Returns
            -------
            Tuple
                a tuple of status code and html content
            """

        headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54',
        'accept': 't	text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.stackoverflow.com/',
        'accept-language': 'en-US,en;q=0.9',
        }
        read_site = requests.get(url, headers=headers)
        return read_site.status_code, read_site.content

    def __scrap_content(self, content:str, num_of_samples:int) -> None:
        """
            Scrap the Html content to get required sections into a List
        """
        soup = BeautifulSoup(content, "html.parser")
        for info in soup.find_all(class_ = "question-summary"):
            tags = ""
            for tag in info.find_all("a", "post-tag flex--item"):
                tags = f"{tags} : {tag.text}"


            user = user_url =  ""
            for usr in info.find_all("div", "user-details"):
                user = usr.a.text
                user_url = usr.a['href']

            self.__items.append(
                {
                    'id': info['id'],
                    'question': info.find("h3").text,
                    'question_url': info.a['href'],
                    'summary': info.find("div", "excerpt").text,
                    'tags': tags,
                    'question_time': info.find("span", "relativetime").attrs['title'], 
                    'user': user,  
                    'user_url': user_url,
                    'user_badge': info.find("span", "v-visible-sr").text, 
                    'user_reputation_score': info.find("span", "reputation-score").text, 
                    'votes': info.find("span", "vote-count-post").text,
                    'answer': info.find("div", "status").text,
                    'views': info.find("div", "views").text
                }
            )
            if len(self.__items) >= num_of_samples:
                break


