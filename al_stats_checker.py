import os
import pandas as pd
import shutil
import unicodedata

ROMAN_MAP = {
    "ii": "2",
    "iii": "3",
    "iv": "4", 
    "v": "5"
}

REPLACEMENTS = {
    "µ": "muse"
}

"""
Functionality:
Search ship, compare stats to averages
    -list all stats and compare stats to averages OR just search one particular stat and compare averages
    -opt to compare stats to avg of all ships of the same class, avg of all ships of the same class and rarity,
    or avg all ships of the same class and rarity whose stats are above the median
"""

def main() -> None:
    
   
    ship_data = load_ship_data()
    print_intro()

    while True:
        print("\n1. Explore average stats of a ship.")
        print("2. Compare a ship")
        print("3. Exit")
        choice = str(input("Choose an option by typing the corresponding number: "))  

        if choice == "1":
            show_average_stats()
        elif choice == "2":
            compare_ships()
        elif choice == "3":
            "Exited successfully"
            break
        else:
            print("Please enter a valid input.")

    

    

def load_ship_data() -> dict:
    """
    load all ship data, a dictionary with 32 items: 4 levels for each of the 8 ship hull types
    each key is the name of the ship class and level, e.g. DD_Level_100
    each value is a pandas dataframe of the information
    """
    # data is kept in a folder called ship_stats_data in the same folder as this program
    data_folder = os.path.join(os.path.dirname(__file__), "ship_stats_data")
    ship_data = {}

    # go through every file in the data folder, extract the key for the dict element, 
    # construct a pandas dataframe from the csv data as the value and append the key-value pair
    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):
            key = filename.replace(".csv", "")
            filepath = os.path.join(data_folder, filename)
            df = pd.read_csv(filepath)
            ship_data[key] = df
    
    return ship_data

def print_intro() -> None:
    """
    Called at program start to print the intro
    """
    ascii_art = r"""
                             _                            _        _                                                       
     /\                     | |                          | |      | |                                                      
    /  \    _____   _ _ __  | |     __ _ _ __   ___   ___| |_ __ _| |_ ___    ___ ___  _ __ ___  _ __   __ _ _ __ ___ _ __ 
   / /\ \  |_  / | | | '__| | |    / _` | '_ \ / _ \ / __| __/ _` | __/ __|  / __/ _ \| '_ ` _ \| '_ \ / _` | '__/ _ \ '__|
  / ____ \  / /| |_| | |    | |___| (_| | | | |  __/ \__ \ || (_| | |_\__ \ | (_| (_) | | | | | | |_) | (_| | | |  __/ |   
 /_/    \_\/___|\__,_|_|    |______\__,_|_| |_|\___| |___/\__\__,_|\__|___/  \___\___/|_| |_| |_| .__/ \__,_|_|  \___|_|   
                                                                                                | |                        
                                                                                                |_|                        
    """
    # Get terminal width (default to 80 if unavailable)
    term_width = shutil.get_terminal_size((80, 20)).columns  

    # Center each line
    for line in ascii_art.splitlines():
        print(line.center(term_width))

    print("All stats assume 100 affinity. Data is gathered from the Azur Lane Wiki https://azurlane.koumakan.jp/wiki/List_of_Ships_by_Stats")
    print("\nNote that the information from here does not tell the full story on how powerful a ship is. It considers only raw stats and does not take into account other important factors of ship power such as equipment efficiencies and skills.")
    print("It is intended as a general indicator of strength out of interest, not a determinent of tier.")

def show_average_stats(ship_data: dict) -> None:
    """
    Selected by user entering "1" in the main menu.
    Asks the user to enter the name of a ship they wish to search. Also gives guidelines on how to enter this name.
    User can then list the stats that they want to be shown and instructed how to do so, e.g. luck,firepower,anti-air
    """
    selected_ship = ""
    selected_level = 1
    selected_stats = []

    while True:
        print("\nExplore the average stats of a ship.")
        print("Lookup rules:")
        print("    -For any ship with special character in their names, e.g. Lützow, simply type the most intuitive equivalent, e.g. lutzow.")
        print("    -For muse ships, type the word 'muse' in place of the muse special character, e.g. roon muse")

        selected_ship = str(input("\nSelect ship: "))

        print("Pick the level of the ship at which to show the stats:    -1    -100    -120    125")

        selected_level = str(input("\nSelect level: "))

        print("""Options: luck, speed, health, firepower, anti-air, torpedo, evasion, aviation, oil consumption
              reload, anti-submarine, oxygen, ammunition, accuracy
        """)

def compare_ships(ship_data: dict) -> None:
    print("This functionality is not available yet!")

def normalise_name(name: str) -> str:
    """
    Sets input name to lower case, strips accented letters, replaces word "muse" with muse symbol, replaces 
    numeric characters at the end of a ship name e.g. laffey 2 with the "ii" roman numeral which is how
    it's represented in the data.
    """
    name = name.lower()
    name = strip_accents(name)

    for k, v in REPLACEMENTS.items():
        name = name.replace(v, k)
    for k, v in ROMAN_MAP.items():
        if name.endswith(" " + v):
            name = name.replace(" " + v, " " + k)
    
    return name


def strip_accents(text: str) -> str:
    """
    Filters accented letters like L'Opiniâtre to L'Opiniatre
    """
    decomposed = unicodedata.normalize('NFD', text)
    filtered_chars = []

    for c in decomposed:
        if unicodedata.category(c) != 'Mn':
            filtered_chars.append(c)
    
    return ''.join(filtered_chars)

if __name__ == "__main__":
    main()