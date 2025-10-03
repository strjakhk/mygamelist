from UI import UI
from gameinfo import GameInfo
from datetime import datetime

def main():
    ui = UI()
    ui._clear_console()
    while True:
        try:
            ui.show_context()
        except KeyboardInterrupt:
            ui.quit()


def is_recent(game, year=2):
    """ returns True if the game is recent, false otherwise"""
    released_year = int(game.released.split("-")[0]) # get released year
    current_year = datetime.now().year # get current year
    return (current_year - released_year) <= year

def is_high_score(game, threshold=80):
    """returns True if the game is high score"""
    return game.metacritic >= threshold


def game_to_json(game):
    return game.to_json()

if __name__ == "__main__":
    main()