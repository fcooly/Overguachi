## Overguachi

This is a basic data science project using data from players of [Overwatch](https://playoverwatch.com/en-us/). The project is divided in two steps: scrapping the data using the [OW-API](https://ow-api.com/) and analyzing it with the help of [https://pandas.pydata.org/](https://pandas.pydata.org/). 


## Progress

This is a project in progress, I will update the repository with more files in the close future.

- [x] Upload scrapper file.
- [x] Create Readme.md.
- [ ] Upload data analysis.

## Scrapping the data

The scrapper is pretty simple. The starting point is a list of players to scrap, which for privacity reasons I am not including
in the files of the repository. The code then creates an empty dictionary which will save the statistics in a JSON format.

There are two basic calls to the API:
** - get_profile ** gets the profile of a user if it exists. It must be provided with the battletag, region and platform.
** - get_hero ** gets the stats for a given hero for the specified user. These contain shared stats (number of eliminations, time
spent on fire, etc...) as well as unique stats for the hero, like hook accuracy for Roadhog for example.

There are two important extra functions which are used to retrieve the stats:
** - check_user ** simply loops over the possible platform and region options to check if the user exists in some of them.
** - get_user_stats ** loops over all the heroes for all the players in the player list and retrieves the stats by using API calls.

The data is later stores in a dictionary in JSON structure, which is dumped to a cache file in the disk using pickle.

### Comments

* Note that the API requires the hash symbol in a PC gamertag <code>gamertag#number</code> to be replaced by a hyphen <code>gamertag-number</code>.*
* Also note that, for reasons related to the userlist I was working with, the regions only include US and EU, as well as the platforms only include PC and PS4. The code can be easily modified to include the excluded platform and region.*


## Analyzing the data


## Author

* **[Mario Herrero-Valea](https://github.com/fcooly)** 

## Acknowledgements
I am very thankeful to my Twitter followers and to the community built around the [Ocho sobre Diez podcast](https://twitter.com/ochosobrediez) for helping me (by providing data) in the initial steps of this project.
