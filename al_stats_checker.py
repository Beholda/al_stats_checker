import os
import pandas as pd
import shutil

"""
Functionality:

"""

def main() -> None:
    
   
    ship_data = load_ship_data()
    print_intro()
    
        
    # data_folder = os.path.join(os.path.dirname(__file__), "ship_stats_data")
    # df = pd.read_csv(os.path.join(data_folder, "BB_Level_125.csv"))
    # # print(df.head())
    # # print(df["Luck"])
    # sr_bb_mean_fp = df[df["Rarity"] == "Super Rare"]
    # ur_bb_mean_fp = df[df["Rarity"] == "Ultra Rare"]

    # median_fp = int(sr_bb_mean_fp["Firepower"].median())
    # mean_fp = int(sr_bb_mean_fp["Firepower"].mean())

    # print(f"The median firepower is {median_fp}")
    # print(f"The mean firepower is {mean_fp}")

    # sr_fp_vals = sr_bb_mean_fp["Firepower"]
    # ur_fp_vals = ur_bb_mean_fp["Firepower"]
    # ships_below_avg = (sr_fp_vals < mean_fp).sum()
    # ships_above_avg = (sr_fp_vals >= mean_fp).sum()

    # print(f"There are {ships_below_avg} SR and UR battleships below the avg of 416 and {ships_above_avg} above it")

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

if __name__ == "__main__":
    main()