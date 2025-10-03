import requests
import os
from dotenv import load_dotenv

class GameInfo:
    """GameInfo class is an implementation of the api RAWG to get informatimon of every game"""

    def __init__(self):
        # if file e.env doesn't exist then raise a generic error.
        if not load_dotenv("e.env"):
            raise SystemExit("file e.env doesn't exist. Please read instructions from README.md")
        
        # load the api key from the env variable
        self._api_key = os.getenv("API_KEY")

        self._url = "https://api.rawg.io/api/games"
        self._genres = [
            "action",
            "indie",
            "adventure",
            "RPG",
            "strategy",
            "shooter",
            "casual",
            "simulation",
            "puzzle",
            "arcade",
            "platformer",
            "massively multiplayer",
            "racing",
            "sports",
            "fighting",
            "family",
            "board games",
            "card",
            "educational1"

        ]
        self._ordering_keywords = [
            "metacritic",
            "-metacritic",
            "name",
            "-name",
            "released",
            "-released"
        ]
    
    @property
    def url(self):
        return self._url

    @property
    def api_key(self):
        return self._api_key
    
    @property
    def ordering_keywords(self):
        return self._ordering_keywords

    @property
    def genres(self):
        return self._genres

    def _request(self, payload: dict) -> list[dict]:
        r = requests.get(self.url, payload)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            raise SystemExit("HTTPError")
        if r.json().get("error"):
            raise SystemExit("Invalid API KEY")
        
        return r.json()["results"]

    def _check_page_number(self, n: int):
        if not 1 <= n <= 100:
            raise ValueError("Invalid page number")
        
    def _check_ordering_method(self, name: str):
        if name not in self.ordering_keywords:
            raise ValueError("Invalid ordering method")

    def search_by_name(self, name: str) -> list[dict]:
        """
        search games by name
        
        :param name: keyword to search
        :type name: str
        :returns: a list of games matching the keyword 'name'
        :rtype: list

        """
        name = name.strip()

        payload = {"key": self.api_key, "search": name}
        return self._request(payload)
    
    def search_by_metacritic(self, score: tuple, ordering: str="-metacritic", page:int=1) -> list[dict]:
        
        """
        serach games by its metacritic score.

        :param score: score range (ie 96, 100)
        :type score: tuple(int)
        :param ordering: ordering methods available: metacritic, name, released. Invert with '-' (-name). Defaults to ``-metacritic``
        :type ordering: str
        :param page: number of page to search for if the number of items is greater than 20. Defaults to ``1``
        :type page: int
        :returns: a list of games matching the minimum metacritic score. Maximum items: 20
        :rtype: list

        """
        min, max = score
        if not 0 <= min <= 100 and 0 <= max <= 100:
            raise ValueError("Invalid metacritic score")
        
        # raises a ValueError if the page number is out of range
        self._check_page_number(page)        
        # raises a ValueError if the ordering method is invalid
        self._check_ordering_method(ordering)
        
        payload = {"key":self.api_key, "metacritic": ",".join((str(min), str(max))), "ordering": ordering, "page": page}

        return self._request(payload)

    def search_by_genre(self, genre: str, ordering: str="-metacritic", page:int=1) -> list[dict]:
        """
        search games by genre

        :param genre: genre to search for (availables in object.genres)
        :type genre: str
        :param ordering: ordering methods available: metacritic, name, released. Invert with '-' (-name). Defaults to ``-metacritic``
        :type ordering: str
        :param page: number of page to search for if the number of items is greater than 20. Defaults to ``1``
        :type page: int
        :retnurns: a list of games matching the genre
        :rtype: list

        """

        if genre not in self.genres:
            raise ValueError("Invalid genre")
        
        # raises a ValueError if the page number is out of range
        self._check_page_number(page)        
        # raises a ValueError if the ordering method is invalid
        self._check_ordering_method(ordering)

        payload = {"key":self.api_key, "genres": genre, "ordering": ordering, "page": page}

        return self._request(payload)
    
    def search_by_dates(self, dates: tuple, ordering: str="-metacritic", page:int=1) -> list[dict]:
        """
        search games in the range of the dates given in dates (ie: 2025-01-01,2025-12-31)

        :param dates: a tuple of two dates in the format YYYY-MM-DD
        :type dates: tuple[str,str]
        :param ordering: ordering methods available: metacritic, name, released. Invert with '-' (-name). Defaults to ``-metacritic``
        :type ordering: str
        :param page: number of page to search for if the number of items is greater than 20. Defaults to ``1``
        :type page: int
        :retnurns: a list of games in the range of dates given
        :rtype: list[dict]

        """

        # raises a ValueError if the page number is out of range
        self._check_page_number(page)        
        # raises a ValueError if the ordering method is invalid
        self._check_ordering_method(ordering)

        payload = {"key":self.api_key, "dates":",".join(dates), "ordering": ordering, "page": page}

        return self._request(payload)
