import utils
import scrapping_methods
import sqlite3


def create_basketball_reference_database():    

    with sqlite3.connect('basketball-reference.db') as connection:
            cursor = connection.cursor()

            league_index_items, league_index_data  = scrapping_methods.get_league_index()
            utils.database.create_table(cursor, "league_index", league_index_items)
            utils.database.add_to_table(connection, cursor, "league_index", league_index_data)
            del league_index_data, league_index_items

            player_index_items, player_index_data = scrapping_methods.get_player_index()
            utils.database.create_table(cursor, "player_index", player_index_items)
            utils.database.add_to_table(connection, cursor, "player_index", player_index_data)
            del player_index_data, player_index_items


def main():

    # create_basketball_reference_database()
    scrapping_methods.get_player_data()    

if __name__ == "__main__":
    main()