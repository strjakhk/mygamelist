# MyGameList
Project for CS50p

## Video Demo

https://youtu.be/vtcR9-rW_PE


## Description
This project allows you to consult a global video game database.  
You can search for games by their **Metacritic score**, **name**, or **release date**.  
Once you find a game, you can view its official background image and add it to your personal **favorites list**.  

From the main menu, you can:
- Access your favorites list
- Add or remove games
- Save or export the list in JSON format
- Import a previously saved list when running the program again  

---

## How to Run


1. Install the required dependencies listed in `requirements.txt`:
    
   ```bash
    pip install -r requirements.txt
   ```

For the class **GameInfo** (**gameinfo.py**) to make API requests, an environment file is required:

- Create a file named **.env** in the root directory.
- Inside it, define the variable **API_KEY** with the value of a valid RAWG public API key:

```ini
    API_KEY=your_api_key_here
```


## Program Flow

- The main program logic is located in **project.py** within the **main()** function.

- The main loop begins by instantiating the **UI** class and repeatedly calling the method **ui.show_context()**.

- The context attribute inside the **UI** object determines which interface is displayed.

- For example:
    - If the user selects *Favorites* in the main menu, the context changes to **favorites_context**.
    - Then, **show_context()** will display the corresponding favorites menu.


## Favorites List

The favorites list is implemented as an object with the following methods:

- **add()**: Add a game to the list.

- **remove()**: Remove a game from the list.

- **export_json()**: Save the favorites list to a JSON file (with a fixed filename).

- **import_json()**: Load the favorites list from the saved JSON file.


## Future Improvements

- Allow users to customize the export filename.
- Improve error handling for expired or invalid API keys.
- Expand the interface after selecting a game to show more info about the game.
- Expand the UI to support more interactive features.

