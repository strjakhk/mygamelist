from favorites import Favorites
from game import Game
from gameinfo import GameInfo
from enum import Enum
from tabulate import tabulate
import webbrowser
import sys
import os

class MenuTable:
    """menu tables to use in tabulate """

    # static menus    
    mainmenu = [
        ["1", "search game"],
        ["2", "favorites"],
        ["3", "import favorites"],
        ["4", "export favorites"],
        ["5", "exit"]
    ]

    searchgame = [
        ["1", "search by name"],
        ["2", "search by metacritic"],
        ["3", "search by genre"],
        ["4", "search by dates"],
        ["5", "back"]
    ]

    favorite_selected = [
        ["1", "delete from favorites"],
        ["2", "open game background"],
        ["3", "back"]
    ]

    game_selected = [
        ["1", "add to favorites"],
        ["2", "open game background"],
        ["3", "back"]
    ]

    # dynamic menus
    @staticmethod
    def get_from_list(gamelist: list[Game]) -> list[list[str]]:
        """returns a table list to use in tabulate, similar to the static menus"""
        
        
        menu = [[i + 1, game.released, game.name, game.metacritic] for i, game in enumerate(gamelist)]

        # first row as header
        menu.insert(0, ["id", "Release date", "Name", "Metacritic"])
        
        return menu

class Context(Enum):
    MAINMENU = "mainmenu"
    SEARCH_GAME = "search_game"
    FAVORITES = "favorites"
    GAME_LIST = "game_list"
    GAME_SELECTED = "game_selected"
    IMPORT_FAVORITES = "import_favorites"
    EXPORT_FAVORITES = "export_favorites"
    QUIT = "quit"


class UI:
    """
    This class manages to main flow of the program, including menus, user input and output

    General flow:
    - There must be an instance of this class and a call to ui.show_context() in main()
    - show_context() must be in a While loop, inside main.
    - show_context() will show a context depending the value of UI._current_context
    - the context is basically a menu or ui, represented by a method
    - besides the menu, the context will also manage the user input and options availables.
    
    Usage example:
        ui = UI()
        while True:
            ui.show_context()

    """
    def __init__(self, context = Context.MAINMENU):
        self._current_context = context
        self._previous_context = Context.MAINMENU
        self._contexts = {
            Context.MAINMENU: self.mainmenu,
            Context.SEARCH_GAME: self.search_game,
            Context.FAVORITES: self.my_favorites,
            Context.GAME_LIST: self.game_list,
            Context.GAME_SELECTED: self.game_selected,
            Context.IMPORT_FAVORITES: self.import_favorites,
            Context.EXPORT_FAVORITES: self.export_favorites,
            Context.QUIT: self.quit
        }

        # maange the favorites list in favorites.favorites. Also manage import and export favorites.
        self._favorites: Favorites = Favorites()

        # when using methods like "search_by", result lists of games will be saved in this attribute to be shown in context GAME_LIST
        self._game_list: list[Game] = []

        # when in context GAME_LIST, the game you select will be saved in this attribute to be shown in context GAME_SELECTED
        self._game_selected: Game = None

        # class to manage api requests
        self._game_info = GameInfo()

    
    @property
    def favorites(self):
        return self._favorites

    def show_context(self):
        """shows the current context"""
        self._clear_console()
        self._contexts[self._current_context]()
    
    def _clear_console(self):
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

    def _update_context(self, new_context: Context, explicit_previous_context: Context = None):
        if not explicit_previous_context:
            self._previous_context = self._current_context
        else:
            self._previous_context = explicit_previous_context
        self._current_context = new_context

    def _print_header(self, header: str):
        print("")    
        print(tabulate([["", "", "", header, ""]], tablefmt="plain"))
    
    def _print_menu(self, menutable: list, header: str="", tablefmt: str="outline"):
        print(tabulate(menutable, headers=header, tablefmt=tablefmt))

    def _load_options(self, options: dict, label: str="option: "):
        opt = input(label).strip()
        action = options.get(opt)
        if action:
            action()

    # Contexts

    def mainmenu(self):

        # prints the menu
        self._print_header("My Game List")
        self._print_menu(MenuTable.mainmenu)

        # loads options and wait for the user input
        self._load_options({
            "1": lambda: self._update_context(Context.SEARCH_GAME),
            "2": lambda: self._update_context(Context.FAVORITES),
            "3": lambda: self._update_context(Context.IMPORT_FAVORITES),
            "4": lambda: self._update_context(Context.EXPORT_FAVORITES),
            "5": lambda: self._update_context(Context.QUIT),
        })

    def search_game(self):
        # prints the menu
        self._print_header("Search options")
        self._print_menu(MenuTable.searchgame)

        # loads options and wait for the user input
        self._load_options({
            "1": self._search_by_name,
            "2": self._search_by_metacritic,
            "3": self._search_by_genre,
            "4": self._search_by_dates,
            "5": lambda: self._update_context(self._previous_context),
        })

    def my_favorites(self):
        # prints the menu
        self._print_header("favorites")
        self._print_menu(MenuTable.get_from_list(self.favorites.favorites), header="firstrow")

        # implementar opciones

        options = {str(i + 1): lambda game=game: self._select_game(game) for i, game in enumerate(self.favorites.favorites)}
        options["0"] = lambda: self._update_context(self._previous_context, explicit_previous_context=Context.MAINMENU)
        self._load_options(options, label="game id to select: (0 to go back): ")

    def game_list(self):
        # prints the menu
        self._print_header("results...")
        self._print_menu(MenuTable.get_from_list(self._game_list), header="firstrow")

        # implementar opciones

        options = {str(i + 1): lambda game=game: self._select_game(game) for i, game in enumerate(self._game_list)}
        options["0"] = lambda: self._update_context(self._previous_context, explicit_previous_context=Context.MAINMENU)

        self._load_options(options, label="game id to select: (0 to go back): ")

    def game_selected(self):
        game_table = MenuTable.get_from_list([self._game_selected])
        self._print_menu(game_table, header="firstrow")
        print("")

        if self._previous_context == Context.FAVORITES:
            # juego seleccionado de favoritos
            self._print_menu(MenuTable.favorite_selected, tablefmt="simple")
            self._load_options({
                "1": lambda: self._remove_from_favorites(),
                "2": lambda: self._open_image(self._game_selected.background_url),
                "3": lambda: self._update_context(self._previous_context, Context.MAINMENU)
            }, label="option: ")
        else:
            # juego seleccionado de resultados
            self._print_menu(MenuTable.game_selected, tablefmt="simple")
            self._load_options({
                "1": lambda: self._add_to_favorites(),
                "2": lambda: self._open_image(self._game_selected.background_url),
                "3": lambda: self._update_context(self._previous_context, Context.MAINMENU)
            }, label="option: ")

    def import_favorites(self):
        self._print_menu([["filename:", self.favorites.filename]], tablefmt="simple")
        try:
            self.favorites.import_json()
            self._print_menu([[":)", "file imported successfully"]], tablefmt="simple")
            self._print_menu([["0", "back"]], tablefmt="simple")
            self._load_options({
                "0": lambda: self._update_context(self._previous_context, Context.MAINMENU)
            })

        except FileNotFoundError:
            self._print_menu([[":(", "file not found"]], tablefmt="simple")
            self._print_menu([["0", "back"], ["1", "try again"]], tablefmt="simple")
            self._load_options({
                "0": lambda: self._update_context(self._previous_context, Context.MAINMENU),
                "1": lambda: self._update_context(self._current_context, Context.MAINMENU)
            })

    def export_favorites(self):
        if self.favorites.favorites:
            self.favorites.export_json()
            self._print_menu([["filename:", self.favorites.filename]], tablefmt="simple")
            self._print_menu([[":)", "file exported successfully"]], tablefmt="simple")
            self._print_menu([["0", "back"]], tablefmt="simple")
            self._load_options({
                "0": lambda: self._update_context(self._previous_context, Context.MAINMENU)
            })
        else:
            self._print_menu([[":(", "nothing to save"]], tablefmt="simple")
            self._print_menu([["0", "back"]], tablefmt="simple")
            self._load_options({
                "0": lambda: self._update_context(self._previous_context, Context.MAINMENU)
            })

    def quit(self):
        print("\nSaliendo...")
        sys.exit(0)
    
    def _select_game(self, game: Game):
        self._game_selected = game
        self._update_context(Context.GAME_SELECTED)

    def _open_image(self, url):
        if url:
            webbrowser.open(url)

    def _add_to_favorites(self):
        self.favorites.add(self._game_selected)
        self._game_selected = None
        self._update_context(self._previous_context, Context.MAINMENU)

    def _remove_from_favorites(self):
        self.favorites.remove(self._game_selected)
        self._game_selected = None
        self._update_context(self._previous_context, Context.MAINMENU)

    # Search methods



    def _search_by_name(self):
        name = input("name: ").strip()
        try:            
            games = self._game_info.search_by_name(name)        
        except SystemExit:
            sys.exit("HTTPError. Probably missing a valid API KEY. please read README.md for requirements")

        self._populate_game_list(games)        
        self._update_context(Context.GAME_LIST)

    def _search_by_metacritic(self):
        while True:
            try:
                print("metacritic score range (ie: min = 91, max = 100)")
                min = int(input("min: ").strip())
                max = int(input("max: ").strip())
                break
            
            except ValueError:
                continue

        try:
            games = self._game_info.search_by_metacritic(score=(min,max))
        except SystemExit:
            sys.exit("HTTPError. Probably missing a valid API KEY. please read README.md for requirements")

        self._populate_game_list(games)        
        self._update_context(Context.GAME_LIST)

    def _search_by_genre(self):
        genre = input("genre: ").strip()
        try:
            games = self._game_info.search_by_genre(genre)
        except SystemExit:
            sys.exit("HTTPError. Probably missing a valid API KEY. please read README.md for requirements")

        self._populate_game_list(games)        
        self._update_context(Context.GAME_LIST)

    def _search_by_dates(self):
        while True:
            try:
                print("date range (ie: min = YYYY-MM-DD, max = YYYY-MM-DD)")
                min = input("min: ").strip()
                max = input("max: ").strip()
                if len(min.split("-")) != 3 or len(max.split("-")) != 3:
                    raise ValueError()
                break
            
            except ValueError:
                continue
        
        try:
            games = self._game_info.search_by_dates(dates=(min, max))
        except SystemExit:
            sys.exit("HTTPError. Probably missing a valid API KEY. please read README.md for requirements")
            
        self._populate_game_list(games)        
        self._update_context(Context.GAME_LIST)


    def _populate_game_list(self, games: list[dict]):
        if games:
            self._game_list.clear()
            for game in games:
                self._game_list.append(
                    Game(
                        game["name"],
                        game["released"],
                        game["genres"],
                        game["metacritic"],
                        game["background_image"]
                    )
                )