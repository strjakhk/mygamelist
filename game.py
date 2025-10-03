import csv

class Game:
    def __init__(self, name: str, released: str, genres: tuple, metacritic: int, background_url: str):
        self._name = name
        self._released = released
        self._genres = genres
        self._metacritic = metacritic
        self._background_url = background_url
    

    @property
    def name(self):
        return self._name
    
    @property
    def released(self):
        return self._released
    
    @property
    def genres(self):
        return self._genres

    @property
    def metacritic(self):
        return self._metacritic
    
    @property
    def background_url(self):
        return self._background_url


    def to_json(self):
        return {
            "released": self.released,
            "name": self.name,
            "genres": self.genres,
            "metacritic": self.metacritic,
            "background_url": self.background_url
        }
    

    def __eq__(self, other):
        if isinstance(other, Game):
            return self.name == other.name and self.released == other.released
        else:
            return False

    def __str__(self):
        return self.name