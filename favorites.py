from game import Game
import json

class Favorites:
    def __init__(self):
        self._favorites: list[Game] = []
        self._filename = "favorites.json"


    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self, name: str):
        if not name.endswith(".json"):
            raise ValueError("File extension must be json")
        
        self._filename = name

    @property
    def favorites(self):
        return self._favorites
    
    def _check_instance(self, game: Game):
        if not isinstance(game, Game):
            raise ValueError("game must be instance of class Game")

    def add(self, game: Game):
        self._check_instance(game)
        
        if game in self.favorites:
            raise ValueError(f"{game} already exists in Favorites")
        
        self.favorites.append(game)

    
    def remove(self, game: Game):
        self._check_instance(game)

        try:
            self.favorites.remove(game)
        except ValueError:
            raise ValueError(f"{game} is not in Favorites")
            
        
        
    def export_json(self):
        with open(self.filename, "w") as f:
            favorites = [game.to_json() for game in self.favorites]
            json.dump(favorites, f)

    
    def import_json(self):
        with open(self.filename, "r") as f:
            try:
                game_list = json.load(f)
                self._favorites = [Game(
                    released=game["released"],
                    name=game["name"],
                    genres=game["genres"],
                    metacritic=game["metacritic"],
                    background_url=game["background_url"]
                ) for game in game_list]
            
            except json.JSONDecodeError:
                raise FileNotFoundError("Incorrect file type")
                        

    