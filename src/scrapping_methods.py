import utils


basketball_reference_url = "https://www.basketball-reference.com/"


@staticmethod
def get_league_index(proxies: dict = None) -> list: 

    url = f"{basketball_reference_url}/leagues/"
    
    tags = utils.get_relevant_tags(url)

    headers = [
        "season_period", 
        "season_link", 
        "league_name", 
        "champion_name",
        "champion_link", 
        "mvp_name", 
        "mvp_link", 
        "roy_name", 
        "roy_link",
        "points_leader_name", 
        "points_leader_link", 
        "points",
        "rebound_leader_name", 
        "rebound_leader_link",
        "rebounds",
        "assists_leader_name", 
        "assists_leader_link", 
        "assists",
        "win_share_name", 
        "win_share_link", 
        "win_share"
    ]

    data = []

    for tag_set in tags:

        season_tag = tag_set[0]
        season_period = season_tag.getText()
        season_a_tag = season_tag.find("a")
        season_link = ""
        if season_a_tag is not None:
            season_link = season_tag.find("a").attrs["href"]

        league_tag = tag_set[1]
        league_name = league_tag.getText()

        champion_tag = tag_set[2]
        champion_name = champion_tag.getText()
        champion_a_tag = champion_tag.find("a")
        champion_link = ""
        if champion_a_tag is not None:
            champion_link = champion_tag.find("a").attrs["href"]

        mvp_tag = tag_set[3]
        mvp_name = mvp_tag.getText()
        mvp_a_tag = mvp_tag.find("a")
        mvp_link = ""
        if mvp_a_tag is not None:
            mvp_link = mvp_tag.find("a").attrs["href"]

        roy_tag = tag_set[4]
        roy_name = roy_tag.getText()
        roy_a_tag = roy_tag.find("a")
        roy_link = ""
        if roy_a_tag is not None:
            roy_link = roy_tag.find("a").attrs["href"]

        points_leader_tag = tag_set[5]
        points_leader = points_leader_tag.getText()
        points_leader_a_tag = points_leader_tag.find("a")
        points_leader_link = points_leader_name = points = ""
        if points_leader_a_tag is not None:
            points_leader_link = points_leader_tag.find("a").attrs["href"]
            points_leader_name, points = utils.split_player_stat(points_leader)

        rebound_leader_tag = tag_set[6]
        rebound_leader = rebound_leader_tag.getText()
        rebound_leader_a_tag = rebound_leader_tag.find("a")
        rebound_leader_link = rebound_leader_name = rebounds = ""
        if rebound_leader_a_tag is not None:
            rebound_leader_link = rebound_leader_tag.find("a").attrs["href"]
            rebound_leader_name, rebounds = utils.split_player_stat(rebound_leader)

        assists_leader_tag = tag_set[7]
        assists_leader = assists_leader_tag.getText()
        assists_leader_a_tag = assists_leader_tag.find("a")
        assists_leader_link = assists_leader_name = assists = ""
        if assists_leader_a_tag is not None:
            assists_leader_link = assists_leader_tag.find("a").attrs["href"]
            assists_leader_name, assists = utils.split_player_stat(assists_leader)

        win_share_tag = tag_set[8]
        win_share_data = win_share_tag.getText()
        win_share_a_tag = win_share_tag.find("a")
        win_share_link = ""
        if win_share_a_tag is not None:
            win_share_link = win_share_tag.find("a").attrs["href"]
            win_share_name, win_share = utils.split_player_stat(win_share_data)

        data.append((season_period, season_link, league_name, champion_name,\
                            champion_link, mvp_name, mvp_link, roy_name, roy_link,\
                                points_leader_name, points_leader_link, points, \
                                    rebound_leader_name, rebound_leader_link, rebounds,
                                    assists_leader_name, assists_leader_link, assists, \
                                        win_share_name, win_share_link, win_share))
        

    return (headers, data)