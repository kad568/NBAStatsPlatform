from requests import get
from bs4 import BeautifulSoup as bs
import sqlite3


basketball_reference_url = "https://www.basketball-reference.com/"
league_index_url = f"{basketball_reference_url}/leagues/"
database_name = "basketball_reference.db"

class utils:

    @staticmethod
    def split_player_stat(player_stat: str) -> list:
        split_string = player_stat.split(' ')
        name = " ".join(split_string[:1])
        stat = split_string[2][1:-1]
        return name, stat


class database:

    @staticmethod
    def init_database(database_name: str = database_name):
        sql_connection = sqlite3.connect(database_name)
        database_cursor = sql_connection.cursor() 
        return sql_connection, database_cursor

    @staticmethod
    def create_table(database_cursor, table_name:str, table_items: list, data: list):
        table_items_string = ", ".join(table_items)
        database_cursor.execute(f"CREATE TABLE {table_name}({table_items_string})")

        result = database_cursor.execute("SELECT name FROM sqlite_master")
        available_tables = result.fetchone()
        assert table_name in available_tables, f"{table_name} table not created"
    
    @staticmethod
    def add_to_table(sql_connection, database_cursor, tmp_table_name: str, data: list):

        num_of_data_sets = len(data)
        tmp_data_slots = ', '.join(["?"] * num_of_data_sets)
        database_cursor.executemany(f"INSERT INTO {tmp_table_name} VALUES({tmp_data_slots})", data)
        sql_connection.commit()


def get_league_index(target_url: str = league_index_url, proxies: dict = None) -> list:

    response = get(target_url, proxies=proxies)
    status_code = response.status_code
    
    assert status_code == 200, f"Connection failed with error code {status_code}."

    soup = bs(response.content, 'html.parser')
    league_index_tags = [list(tag.find_all(["th", "td"]))\
                          for tag in list(soup.find_all("tr"))[2:]]

    league_index_item = {
    "season_period": "",
    "season_link": "",
    "league_name": "",
    "champion_name": "",
    "champion_link": "",
    "mvp_name": "",
    "mvp_link": "",
    "roy_name": "",
    "roy_link": "",
    "points_leader_name": "",
    "points_leader_link": "",
    "points": "",
    "rebounds_leader_name": "",
    "rebounds_leader_link": "",
    "rebounds": "",
    "assists_leader_name": "",
    "assists_leader_link": "",
    "assists": "",
    "win_share_name": "",
    "win_share": ""
    } # note - does this need to be created here, makes code bulky

    orig_dict_len = len(league_index_data)

    league_index_data = []

    for tag_set, index in enumerate(league_index_tags):

        season_tag = tag_set[0]
        league_index_item['season_period'] = season_tag.getText()
        season_a_tag = season_tag.find("a")
        if season_a_tag is not None:
            league_index_item['season_link'] = season_tag.find("a").attrs["href"]

        league_tag = tag_set[1]
        league_index_item['league_name'] = league_tag.getText()

        champion_tag = tag_set[2]
        league_index_item['champion_name'] = champion_tag.getText()
        champion_a_tag = champion_tag.find("a")
        if champion_a_tag is not None:
            league_index_item['champion_link'] = champion_tag.find("a").attrs["href"]

        mvp_tag = tag_set[3]
        league_index_item['mvp_name'] = mvp_tag.getText()
        mvp_a_tag = mvp_tag.find("a")
        if mvp_a_tag is not None:
            league_index_item['mvp_link'] = mvp_tag.find("a").attrs["href"]

        roy_tag = tag_set[4]
        league_index_item['roy_name'] = roy_tag.getText()
        roy_a_tag = roy_tag.find("a")
        if roy_a_tag is not None:
            league_index_item['roy_name'] = roy_tag.find("a").attrs["href"]

        points_leader_tag = tag_set[5]
        points_leader = points_leader_tag.getText()
        points_leader_a_tag = points_leader_tag.find("a")
        if points_leader_a_tag is not None:
            league_index_item['points_leader_link'] = points_leader_tag.find("a").attrs["href"]
        league_index_item['points_leader_name'], league_index_item['points'] = utils.split_player_stat(points_leader)

        rebound_leader_tag = tag_set[6]
        rebound_leader = rebound_leader_tag.getText()
        rebound_leader_a_tag = rebound_leader_tag.find("a")
        rebound_leader_sub_link = ""
        if rebound_leader_a_tag is not None:
            league_index_item['rebound_leader_link'] = rebound_leader_tag.find("a").attrs["href"]
        league_index_item['rebound_leader_name'], league_index_item['rebound'] = utils.split_player_stat(rebound_leader)

        assists_leader_tag = tag_set[7]
        assists_leader = assists_leader_tag.getText()
        assists_leader_a_tag = assists_leader_tag.find("a")
        assists_leader_sub_link = ""
        if assists_leader_a_tag is not None:
            assists_leader_sub_link = assists_leader_tag.find("a").attrs["href"]
        assists_leader_name, assists = utils.split_player_stat(assists_leader)

        win_share_tag = tag_set[8]
        win_share_data = win_share_tag.getText()
        win_share_a_tag = win_share_tag.find("a")
        win_share_sub_link = ""
        if win_share_a_tag is not None:
            win_share_sub_link = win_share_tag.find("a").attrs["href"]
        win_share_name, win_share = utils.split_player_stat(win_share_data)

        current_dict_len = len(league_index_item)
        assert current_dict_len == orig_dict_len

        league_index_data.append((season_period, season_sub_link, league_name, champion_name,\
                              champion_sub_link, mvp_name, mvp_sub_link, roy_name, roy_sub_link,\
                                 points_leader_name, points, rebound_leader_name, rebounds,\
                                     assists_leader_name, assists, win_share_name, win_share))

        return (league_index_item_names, league_index_data)
    
def create_basketball_reference_database(table_name, table_items, data):

    sql_connection, database_cursor = database.init_database()
    database.create_table(database_cursor, table_name, table_items)
    database.add_to_table(sql_connection, database_cursor, table_name, data)

def main():

    tables = list(data.keys())

    data  = {"league_index": get_league_index()}

    create_basketball_reference_database(data)

if __name__ == "__main__":
    main()