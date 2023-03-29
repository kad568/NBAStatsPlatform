import utils
import scrapping_methods
import sqlite3


    
def create_basketball_reference_database():

    basketball_reference_url = "https://www.basketball-reference.com/"
    league_index_url = f'{basketball_reference_url}/leagues'    

    headers = [
    "season", 
    "league", 
    "champion",
    "mvp", 
    "roy", 
    "points_leader",
    "rebounds_leader",
    "assists_leader", 
    "win_share_leader"
    ]

    with sqlite3.connect('basketball-reference.db') as connection:
            cursor = connection.cursor()

            league_index_items, league_index_data  = scrapping_methods.get_table_data(league_index_url, headers)

            utils.database.create_table(cursor, "league_index", league_index_items)
            utils.database.add_to_table(connection, cursor, "league_index", league_index_data)


def main():

    # create_basketball_reference_database()
    with sqlite3.connect('basketball-reference.db') as connection:
        for _ in  utils.database.search(connection, 'league_index', 'points_leader'):
            print(_)


if __name__ == "__main__":
    main()