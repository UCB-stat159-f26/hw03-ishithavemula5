Tennis Career Analysis

This Python package retrieves tennis players' career match data from Tennis Abstract and creates scatter plots showing the age difference between a player and their opponents. 

Installation

The package can be installed directly from GitHub using:

bash
pip install git+https://github.com/UCB-stat159-f26/hw03-ishithavemula5.git


Usage

The package contains two main functions:

- get_player_matches(player_name): Retrieves a player's career match data and returns the cleaned Pandas DataFrame
- plot_player_matches(matches): Creates a scatter plot showing the player's age with the age difference between the player and their opponents. Colors indicate L or W


Data Processing

The package retrieves  match data from JavaScript files and converts into Pandas DataFrames. One important difference is that female players' files contain their opponents' dates of birth, while male players' files contain their opponents' ages directly. The resulting DataFrame contains the match date, opponent, player age, opponent age, age difference, and match result.

Testing

The package uses pytest to test JavaScript parsing, age calculations, data cleaning, and invalid inputs.

To run the tests:

bash
python -m pytest tests/test_data.py -v


Personal Reflections

In HW2, I was mainly focused on cleaning Serena Williams' match data and recreating the NYT visualization, but his time, I had to think about how to make the same process work for different players without having to manually change the code each time. That meant thinking about how to logically repeat the same code for any variable.

One challenge I encountered was understanding how Tennis Abstract stores its match data. I initially assumed that the files would have the same structure for every player, but found that female players' files contain their opponents' birthdates, whereas male players' files simply had the ages. I had to account for these differences when writing the functions to calculate age differences. 

Another part of the assignment that was new to me was writing automated tests. In my previous assignments, I would usually check whether my code worked by running it and looking at the output. For this assignment, I learned how to use pytest to test individual functions.
