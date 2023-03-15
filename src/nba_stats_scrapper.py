from requests import get
from bs4 import BeautifulSoup as bs


basketball_reference_url = "https://www.basketball-reference.com/"
league_index_url = f"{basketball_reference_url}/leagues/"

def get_league_index(target_url: str = league_index_url, proxies: dict = None) -> list:

    response = get(target_url, proxies=proxies)
    status_code = response.status_code
    
    assert status_code == 200, f"Connection failed with error code {status_code}."

    soup = bs(response.content, 'html.parser')
    league_index_tags = [list(tag.find_all(["th", "td"]))\
                          for tag in list(soup.find_all("tr"))[2:]]

    league_index_data = {}
    for tag_set in league_index_tags:

        season_tag = tag_set[0]
        season_period = season_tag.getText()
        season_a_tag = season_tag.find("a")
        season_sub_link = ""
        if season_a_tag is not None:
            season_sub_link = season_tag.find("a").attrs["href"]

        league_tag = tag_set[1]
        league_name = league_tag.getText()

        champion_tag = tag_set[2]
        champion_name = champion_tag.getText()
        champion_a_tag = champion_tag.find("a")
        champion_sub_link = ""
        if champion_a_tag is not None:
            champion_sub_link = champion_tag.find("a").attrs["href"]

        mvp_tag = tag_set[3]
        mvp_name = mvp_tag.getText()
        mvp_a_tag = mvp_tag.find("a")
        mvp_sub_link = ""
        if mvp_a_tag is not None:
            mvp_sub_link = mvp_tag.find("a").attrs["href"]#

        roy_tag = tag_set[4]
        roy_name = roy_tag.getText()
        roy_a_tag = roy_tag.find("a")
        roy_sub_link = ""
        if roy_a_tag is not None:
            roy_sub_link = roy_tag.find("a").attrs["href"]

        points_leader_tag = tag_set[5]
        points_leader_name = points_leader_tag.getText()
        points_leader_a_tag = points_leader_tag.find("a")
        points_leader_sub_link = ""
        if points_leader_a_tag is not None:
            points_leader_sub_link = points_leader_tag.find("a").attrs["href"]

        rebound_leader_tag = tag_set[6]
        rebound_leader_name = rebound_leader_tag.getText()
        rebound_leader_a_tag = rebound_leader_tag.find("a")
        rebound_leader_sub_link = ""
        if rebound_leader_a_tag is not None:
            rebound_leader_sub_link = rebound_leader_tag.find("a").attrs["href"]

        assists_leader_tag = tag_set[7]
        assists_leader_name = assists_leader_tag.getText()
        assists_leader_a_tag = assists_leader_tag.find("a")
        assists_leader_sub_link = ""
        if assists_leader_a_tag is not None:
            assists_leader_sub_link = assists_leader_tag.find("a").attrs["href"]

        win_share_tag = tag_set[8]
        win_share_name = win_share_tag.getText()
        win_share_a_tag = win_share_tag.find("a")
        win_share_sub_link = ""
        if win_share_a_tag is not None:
            win_share_sub_link = win_share_tag.find("a").attrs["href"]
            

if __name__ == "__main__":

    get_league_index()