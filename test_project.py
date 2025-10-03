import pytest
from game import Game
from project import is_recent, is_high_score, game_to_json

@pytest.fixture
def my_game():
    return Game(
        name="Half-life 2",
        released="2004-11-16", # also my birthday :)
        genres=("action", "shooter"),
        metacritic=96,
        background_url="https://media.rawg.io/media/games/b8c/b8c243eaa0fbac8115e0cdccac3f91dc.jpg"
    )


def test_is_recent(my_game):
    assert not is_recent(my_game)


def test_is_high_score(my_game):
    assert is_high_score(my_game)


def test_game_to_json(my_game):
    assert game_to_json(my_game).get("name") != None