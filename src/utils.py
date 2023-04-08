from requests import get
from bs4 import BeautifulSoup as bs
import sqlite3


headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }


class database:

    database_name = "basketball_reference.db"   

    @staticmethod
    def create_table(database_cursor, table_name:str, table_items: list):

        table_items_string = ", ".join(table_items)
        database_cursor.execute(f"CREATE TABLE {table_name}({table_items_string})")
    
    @staticmethod
    def add_to_table(sql_connection, database_cursor, tmp_table_name: str, data: list):

        num_of_data_sets = len(data[0])
        tmp_data_slots = ', '.join(["?"] * num_of_data_sets)
        database_cursor.executemany(f"INSERT INTO {tmp_table_name} VALUES({tmp_data_slots})", data)
        sql_connection.commit()
    
    @staticmethod
    def search(sql_connection, table_name, search_header):

        result = sql_connection.execute(f"SELECT {search_header} FROM {table_name}")

        return result.fetchall()

def get_relevant_tags(target_url: str, proxies: dict = None, tag_types: list = ["tr", ["th", "td"]]) -> list[list]:

    response = get(target_url, proxies=proxies, headers=headers)
    status_code = response.status_code
    
    assert status_code == 200, f"Connection failed with error code {status_code}."

    soup = bs(response.content, 'lxml')
    tags = [list(tag.find_all(tag_types[1]))\
                    for tag in list(soup.find_all(tag_types[0]))[2:]]
    
    return tags
