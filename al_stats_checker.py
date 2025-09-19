import os
import pandas as pd
import shutil
import unicodedata
from typing import Optional, Tuple

# mapping users inputs of numerals to roman numerals
# only ii is really used at time of writing (for sequel ships like houston ii)
ROMAN_MAP = {
    "ii": "2",
    "iii": "3",
    "iv": "4", 
    "v": "5"
}

SYMBOLS = {
    "µ": "muse"
}

VALID_STATS = {
    "luck": "Luck",
    "speed": "Speed",
    "health": "Health",
    "firepower": "Firepower",
    "anti-air": "Anti-Air",
    "torpedo": "Torpedo",
    "evasion": "Evasion",
    "aviation": "Aviation",
    "oil consumption": "Oil Consumption",
    "reload": "Reload",
    "anti-submarine": "Anti-Submarine",
    "oxygen": "Oxygen",
    "ammunition": "Ammunition",
    "accuracy": "Accuracy",
    "all": "all"  # special keyword
}

VALID_LEVELS = ["1", "100", "120", "125"]

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
            show_average_stats(ship_data)
        elif choice == "2":
            compare_ships(ship_data)
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

        selected_ship = str(input("\nSelect ship: ")).strip()

        print("Pick the level of the ship at which to show the stats.")
        print("Options: 1, 100, 120, 125")

        selected_level = str(input("\nSelect level: "))

        if selected_level not in VALID_LEVELS:
            print("Please choose from the options.")
            continue

        ship_row, class_df = find_ship(selected_ship, selected_level, ship_data)

        if ship_row is None:
            print(f"Ship '{selected_ship}' not found at level {selected_level}. Please try again.")
            continue

        print(f"Options: {", ".join(sorted(VALID_STATS))}")
        print("Separate each choice by commas e.g. speed,anti-air,firepower,oil consumption,reload")


        while True:
            stats_input = input("\nSelect stats: ")
            invalid = []
            selected_stats.clear()  # reset for each input attempt

            for stat in stats_input.split(","):
                cleaned = stat.strip().lower()
                if cleaned in VALID_STATS:
                    selected_stats.append(VALID_STATS[cleaned])  # store proper DF column name
                else:
                    invalid.append(cleaned)

            if invalid:
                print(f"INVALID INPUT(S): {', '.join(invalid)}")
                print("Please choose from:", ", ".join(sorted(VALID_STATS)))
                continue  # re-prompt the user

            # Handle 'all' AFTER input validation
            if "all" in stats_input.lower():  # check if user typed 'all'
                selected_stats = []
                for col in VALID_STATS.values():
                    if col != "all":
                        selected_stats.append(col)

            break  # input is valid, exit loop

        
        # comparisons are always only done with ships within the same class as that's what's relevant
        # compare this ship's stats to means and medians of all ships
        # compare this ship's stats to means and medians of all ships of the same rarity
        # compare this ship's stats to means and medians of all ships whose stats are above the median
        # (the idea of the above is to compare it to the ships that are "good")
        # show where this ship is ranked in that stat among all ships
        while True:
            print("\nSelect which metric by which you wish to compare this ship's stats.")
            print("Note that metrics are drawn only from the ships of the same class as this ship.")
            print("Subsets of a class are simply considered to be within that class. For example, battlecruisers are considered battleships for simplicity")
            
            for key, (desc, _) in AVERAGE_STATS_OPTIONS.items():
                print(f"{key}. {desc}")
            
            choice = input("Enter choice: ").strip()
            if choice in AVERAGE_STATS_OPTIONS:
                _, func = AVERAGE_STATS_OPTIONS[choice]
                func(ship_row, class_df, selected_stats)
            else:
                print("Invalid choice, please try again.")
            
            print("\n1. Make another comparison\n2. Exit to main menu")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                break
            else:
                return

def compare_ships(ship_data: dict) -> None:

    first_ship = ""
    second_ship = ""
    selected_level = 1
    stats_input = ""
    selected_stats = []
    invalid = []

    while True:
        print("\nCompare the stats of two ships.")
        print("Lookup rules:")
        print("-For any ship with special character in their names, e.g. Lützow, simply type the most intuitive equivalent, e.g. lutzow.")
        print("-For muse ships, type the word 'muse' in place of the muse special character, e.g. roon muse")

        first_ship = str(input("\nSelect first ship for comparison: ")).strip()
        second_ship = str(input("Select second ship for comparison: ")).strip()

        print("Pick the level of the ships at which to show the stats.")
        print("Options: 1, 100, 120, 125")

        selected_level = str(input("\nSelect level: "))

        if selected_level not in VALID_LEVELS:
            print("Please choose from the options.")
            continue

        first_ship_row, first_class_df = find_ship(first_ship, selected_level, ship_data)

        if first_ship_row is None:
            print(f"Ship '{first_ship}' not found at level {selected_level}. Please try again.")
            continue

        second_ship_row, second_class_df = find_ship(second_ship, selected_level, ship_data)

        if second_ship_row is None:
            print(f"Ship '{second_ship}' not found at level {selected_level}. Please try again.")
            continue

        # Ensure both ships are from the same dataframe
        if first_class_df is not second_class_df:
            print(f"\nNote that {first_ship_row["Ship Name"]} and {second_ship_row["Ship Name"]} are not the same class!.")
            print(f"{first_ship_row["Ship Name"]} is a {first_ship_row["Type"]} while {second_ship_row['Ship Name']} is a {second_ship_row["Type"]}.")

        print(f"\nOptions: {", ".join(sorted(VALID_STATS))}")
        print("Separate each choice by commas e.g. speed,anti-air,firepower,oil consumption,reload")

        while True:
            stats_input = input("\nSelect stats: ")
            invalid = []
            selected_stats.clear()  # reset for each input attempt

            for stat in stats_input.split(","):
                cleaned = stat.strip().lower()
                if cleaned in VALID_STATS:
                    selected_stats.append(VALID_STATS[cleaned])  # store proper DF column name
                else:
                    invalid.append(cleaned)

            if invalid:
                print(f"INVALID INPUT(S): {', '.join(invalid)}")
                print("Please choose from:", ", ".join(sorted(VALID_STATS)))
                continue  # re-prompt the user
   
            # Handle 'all' AFTER input validation
            if "all" in stats_input.lower():  # check if user typed 'all'
                selected_stats = []
                for col in VALID_STATS.values():
                    if col != "all":
                        selected_stats.append(col)
            break  # input is valid, exit loop

        while True:
            # call the function to actually compare the two ships
            compare_two_ships(first_ship_row, second_ship_row, selected_stats)

            # Ask the user what to do next
            print("\n1. Compare another pair of ships")
            print("2. Exit to main menu")

            next_choice = input("Enter choice: ").strip()
            if next_choice == "1":
                break  # break this inner loop to re-prompt for new ships
            elif next_choice == "2":
                return  # exit the compare_ships function to go back to main menu
            else:
                print("Invalid choice, returning to main menu.")
                return

def normalise_name(name: str) -> str:
    """
    Normalises ship names:
    - lowercase
    - strip accents
    - convert 'muse' keyword
    - replace 'ß' with 'ss'
    - handle roman numerals
    - handle 'retrofit' keyword
    """
    name = name.lower().strip()
    name = strip_accents(name)
    name = name.replace("ß", "ss")

    # replace "retrofit" with " (retrofit)" so it matches data
    if "retrofit" in name and "(retrofit)" not in name:
        name = name.replace("retrofit", "").strip() + " (retrofit)"

    for k, v in SYMBOLS.items():
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

def compare_to_all(ship_row: pd.Series, class_df: pd.DataFrame, stats: list[str]) -> None:
    """
    Compare this ship's stats to the mean/median of all ships in its class at this level.
    """
    for stat in stats:
        ship_value = ship_row[stat]
        stat_series = class_df[stat].dropna()

        mean_val = stat_series.mean()
        median_val = stat_series.median()

        rank = (stat_series > ship_value).sum() + 1

        print(f"\nComparison for '{ship_row['Ship Name']}' ({stat}) at this level:")
        print(f"Value: {ship_value}")
        print(f"Mean of all ships: {mean_val:.1f}")
        print(f"Median of all ships: {median_val:.1f}")
        print(f"Rank: {rank} out of {len(stat_series)} ships")

def compare_to_rarity(ship_row: pd.Series, class_df: pd.DataFrame, stats: list[str]) -> None:
    """
    Compare this ship's stats to the mean/median of all ships in its class
    with the same rarity at this level.
    """
    rarity = ship_row["Rarity"]

    # Filter class_df down to only ships of the same rarity
    rarity_df = class_df[class_df["Rarity"] == rarity]

    for stat in stats:
        ship_value = ship_row[stat]
        stat_series = rarity_df[stat].dropna()

        mean_val = stat_series.mean()
        median_val = stat_series.median()
        rank = (stat_series > ship_value).sum() + 1

        print(f"\nComparison for '{ship_row['Ship Name']}' ({stat}) among {rarity} ships at this level:")
        print(f"Value: {ship_value}")
        print(f"Mean of {rarity} ships: {mean_val:.1f}")
        print(f"Median of {rarity} ships: {median_val:.1f}")
        print(f"Rank: {rank} out of {len(stat_series)} {rarity} ships")


def compare_to_above_median(ship_row: pd.Series, class_df: pd.DataFrame, stats: list[str]) -> None:
    """
    Compare this ship's stats to the mean/median of all ships in its class
    above the median (i.e. the mean/median of only the upper half of ships within the stat base).
    This is for purposes of seeing how it compares to the "better" ships.
    """
    for stat in stats:
        ship_value = ship_row[stat]
        stat_series = class_df[stat].dropna()

        median_val = stat_series.median()
        ships_above_median = stat_series[stat_series >= median_val]
        mean_val_of_ships_above_med = ships_above_median.mean()
        median_val_of_ships_above_med = ships_above_median.median()
        rank = (ships_above_median > ship_value).sum() + 1

        rank = (ships_above_median > ship_value).sum() + 1

        print(f"\nComparison for '{ship_row['Ship Name']}' ({stat}) at this level:")
        print(f"Value: {ship_value}")
        print(f"Mean of all ships above the median: {mean_val_of_ships_above_med:.1f}")
        print(f"Median of all ships above the median: {median_val_of_ships_above_med:.1f}")
        print(f"Rank: {rank} out of {len(ships_above_median)} ships")

def find_ship(ship_name: str, ship_level: str, ship_data: dict[str, pd.DataFrame]) -> Tuple[Optional[pd.Series], Optional[pd.DataFrame]]:
    """
    Returns (row, dataframe) for the given ship name at the given level,
    or (None, None) if not found.
    """
    normalized = normalise_name(ship_name)

    for key, df in ship_data.items():
        # key looks like "CV_Level_100"
        if not key.endswith(f"Level_{ship_level}"):
            continue

        matches = df[df["Ship Name"].apply(lambda x: normalise_name(x) == normalized)]
        if not matches.empty:
            return matches.iloc[0], df  # Found the right ship in the right level

    return None, None

AVERAGE_STATS_OPTIONS = {
    "1": ("Compare to mean/median of ships in the same class.", compare_to_all),
    "2": ("Compare to mean/median of ships in the same class with the same rarity.", compare_to_rarity),
    "3": ("Compare to mean/median of only ships in the same class above the median.", compare_to_above_median),
}

def compare_two_ships(first_ship: pd.Series, second_ship: pd.Series, selected_stats: list[str]) -> None:
    for stat in selected_stats:
        first_value = first_ship.get(stat)
        second_value = second_ship.get(stat)

        # Handle missing values
        if pd.isna(first_value) or pd.isna(second_value):
            print(f"\nStat '{stat}' is missing for one or both ships. Skipping comparison.")
            continue

        print(f"\nThe {stat} stat of {first_ship['Ship Name']} is {first_value}.")
        print(f"The {stat} stat of {second_ship['Ship Name']} is {second_value}.")

        if first_value == second_value:
            print(f"{first_ship['Ship Name']} and {second_ship['Ship Name']} have the same {stat} at this level.")
        elif first_value > second_value:
            print(f"{first_ship['Ship Name']} has a higher {stat} than {second_ship['Ship Name']} by {first_value - second_value} at this level.")
        else:
            print(f"{second_ship['Ship Name']} has a higher {stat} than {first_ship['Ship Name']} by {second_value - first_value} at this level.")


if __name__ == "__main__":
    main()