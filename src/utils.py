from requests import get
from bs4 import BeautifulSoup as bs
import sqlite3


class database:

    database_name = "basketball_reference.db"

    @staticmethod
    def init(database_name: str = database_name):

        sql_connection = sqlite3.connect(database_name)
        database_cursor = sql_connection.cursor()

        return sql_connection, database_cursor
    

    @staticmethod
    def create_table(database_cursor, table_name:str, table_items: list):

        table_items_string = ", ".join(table_items)
        database_cursor.execute(f"CREATE TABLE {table_name}({table_items_string})")

        result = database_cursor.execute("SELECT name FROM sqlite_master")
        available_tables = result.fetchone()
        assert table_name in available_tables, f"{table_name} table not created"

    
    @staticmethod
    def add_to_table(sql_connection, database_cursor, tmp_table_name: str, data: list):

        num_of_data_sets = len(data[0])
        tmp_data_slots = ', '.join(["?"] * num_of_data_sets)
        database_cursor.executemany(f"INSERT INTO {tmp_table_name} VALUES({tmp_data_slots})", data)
        sql_connection.commit()


def get_relevant_tags(target_url: str, proxies: dict = None, tag_types: list = ["tr", ["th", "td"]]) -> list[list]:

    response = get(target_url, proxies=proxies)
    status_code = response.status_code
    
    assert status_code == 200, f"Connection failed with error code {status_code}."

    soup = bs(response.content, 'lxml')
    tags = [list(tag.find_all(tag_types[1]))\
                    for tag in list(soup.find_all(tag_types[0]))[2:]]
    
    return tags

def split_player_stat(player_stat: str) -> str:

    split_string = player_stat.split('\xa0')
    name = " ".join(split_string[:1])
    stat = split_string[1][1:-1]

    return name, stat