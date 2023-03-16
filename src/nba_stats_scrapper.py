import utils
import scrapping_methods

    
def create_basketball_reference_database():

    league_index_items, league_index_data  = scrapping_methods.get_league_index()

    sql_connection, database_cursor = utils.database.init()

    utils.database.create_table(database_cursor, "league_index", league_index_items)
    utils.database.add_to_table(sql_connection, database_cursor, "league_index", league_index_data)
    sql_connection.commit()
    sql_connection.close()

def search(header):

    sql_connection, database_cursor = utils.database.init()
    res = sql_connection.execute(f"SELECT {header} FROM league_index")
    for _ in res.fetchall():
        print(_[0])
    sql_connection.close()

def main():

    create_basketball_reference_database()
    search("points")

if __name__ == "__main__":
    main()