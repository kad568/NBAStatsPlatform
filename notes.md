# Notes

* diff between static method and class method
* create a scrapping methods.py, which is then called in main function?
    * class of url, data items to get and method function
* move utils out into own module
    * rename to scrapper_utils
* optimisations league index method
    * add to data object during scrapping not afterwards (save memory)
    * go straight to sql database rather than completing the python list object
    * async? where is the bottle kneck scrapping or adding to database
        * make a queue, where scrapped data is fed in asap at top, adding to database at bottom
            * python continue? yield from?


## To do

* generalise current crapping method
    * pull and store data in the same format as the website
    * store date in tuples (text, link, stat)

# Further ideas

* get shot chart data
* forget getting data myself and use https://pypi.org/project/nba-api/ or use both

### New project ideas

* AI model that takes camera footage and generates data from it
    * auto shot chart for normal person to use
    * auto score board
    * player stats
    * tool to adjust ai mistakes 
    * this tool would support college teams to start using data





##################################################

# To do list

- [x] get all player index & add id (primary key)
- [ ] get all player data and linked to an id


### notes

* find the basketball ref player id (player_id=morrima02)
