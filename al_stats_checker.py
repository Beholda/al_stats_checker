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

VALID_STATS = {
    "luck", "speed", "health", "firepower", "anti-air", "torpedo",
    "evasion", "aviation", "oil consumption", "reload",
    "anti-submarine", "oxygen", "ammunition", "accuracy", "all"
}

AVERAGE_STATS_OPTIONS = {
    "1": ("Compare to mean/median of all ships", compare_to_all),
    "2": ("Compare to mean/median of same rarity", compare_to_rarity),
    "3": ("Compare to ships above average", compare_to_above_average),
    "4": ("Rank this ship among all ships", rank_ship),
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
    stats_input = ""
    selected_stats = []
    invalid = []

    while True:
        print("\nExplore the average stats of a ship.")
        print("Lookup rules:")
        print("-For any ship with special character in their names, e.g. Lützow, simply type the most intuitive equivalent, e.g. lutzow.")
        print("-For muse ships, type the word 'muse' in place of the muse special character, e.g. roon muse")

        selected_ship = str(input("\nSelect ship: "))

        print("Pick the level of the ship at which to show the stats.")
        print("Options: 1, 100, 120, 125")

        selected_level = str(input("\nSelect level: "))

        print(f"Options: {", ".join(sorted(VALID_STATS))}")
        print("Separate each choice by commas e.g. speed,anti-air,firepower,oil consumption,reload")

        while True: 
            stats_input = str(input("\nSelect stats: "))
            for stat in stats_input.split(","):
                cleaned = stat.strip() # remove whitespace
                lowered = cleaned.lower() # make inputs lower case
                selected_stats.append(lowered)

            for stat_validity in selected_stats:
                if stat_validity not in VALID_STATS:
                    invalid.append(stat_validity)
            
            if invalid:
                print(f"INVALID INPUT(S): {', '.join(invalid)}")
                print("Please choose from:", ", ".join(sorted(VALID_STATS)))
            else:
                break
        
        # comparisons are always only done with ships within the same class as that's what's relevant
        # compare this ship's stats to means and medians of all ships
        # compare this ship's stats to means and medians of all ships of the same rarity
        # compare this ship's stats to means and medians of all ships whose stats are above the median
        # (the idea of the above is to compare it to the ships that are "good")
        # show where this ship is ranked in that stat among all ships
        while True:
            print("Select which metric by which you wish to compare this ship's stats.")
            print("Note that metrics are drawn only from the ships of the same class as this ship.")
            print("Subsets of a class are simply considered to be within that class. For example, battlecruisers are considered battleships for simplicity")
            
            for key, (desc, _) in AVERAGE_STATS_OPTIONS.items():
                print(f"{key}. {desc}")
            
            choice = input("Enter choice: ").strip()
            if choice in AVERAGE_STATS_OPTIONS:
                _, func = AVERAGE_STATS_OPTIONS[choice]
                func(selected_ship, selected_level, selected_stats, ship_data)
            else:
                print("Invalid choice, please try again.")

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

def compare_to_all():
    return

def compare_to_rarity():
    return

def compare_to_above_average():
    return

def rank_ship():
    return

if __name__ == "__main__":
    main()