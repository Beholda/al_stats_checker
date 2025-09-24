AL stats checker
By Beholda

This is a simple program written in py to provide information on ship stats in Azur Lane.
It allows users to search the stats of a ship and compare it to the means and medians of several categories of ships.
It also allows for direct comparison between the stats of two ships.

The program has no UI and is presented entirely in the terminal. It hopefully as intuitive instructions on how to use it,
mostly through input in pre-determined specified formats.

Use the .exe file to launch the program. The py source files are also present in full, alongside the scraper program used to obtain
the ship stat data itself.

Libs used: pandas (data management), unicodedata (to assist in ship lookup), pyfiglet (to print the welcome message),
selenium (to scrape the data).

Data source: list of ship stats by Azur Lane wiki.