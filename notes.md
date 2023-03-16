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