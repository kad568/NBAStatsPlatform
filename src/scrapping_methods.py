import utils
from requests import get
from bs4 import BeautifulSoup as bs
from time import sleep, time
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
import pandas as pd
from datetime import datetime


def clean_data(data, headers):

    null_index = []

    for header_index in range(len(data[0])):
        header_data = [data_set[header_index] for data_set in data]

        if all(data == "" for data in header_data):

            null_index.append(header_index)
    
    cleaned_data = []
    for data_set in data:
        cleaned_data_set = [item for index, item in enumerate(data_set) if not index in null_index]
        cleaned_data.append(cleaned_data_set)

    cleaned_headers = [header for index, header in enumerate(headers) if not index in null_index]

    return (cleaned_headers, cleaned_data)


def get_league_index() -> tuple: 

    basketball_reference_url = "https://www.basketball-reference.com"

    url = f'{basketball_reference_url}/leagues'    

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

    orig_headers = headers.copy()
    for index, header in enumerate(orig_headers):
         headers.insert(4 * index + 1, f"{header}_name")
         headers.insert(4 * index + 2, f"{header}_link")
         headers.insert(4 * index + 3, f"{header}_stat")

    data = []

    tags = utils.get_relevant_tags(url)

    for tag in tags:

        data_set = []
        
        for index, header in enumerate(tag):
            
            text = header.getText()

            if header.find("a"):
                link = header.find("a").attrs["href"]
            else:
                 link = ""

            text_splitter = '\xa0'
            if text_splitter in text:
                strings = text.split('\xa0')
                name, stat = strings
                text = ""
            else:
                name = ""
                stat = ""
            
            data_set.append(text)
            data_set.append(name)
            data_set.append(link)
            data_set.append(stat)
        
        data.append(data_set)

    headers, data = clean_data(data, headers)

    return (headers, data)

def get_player_index() -> tuple:

    headers = [
        "player_id",
        "player_name",
        "career_start",
        "career_end",
        "position",
        "height",
        "weight",
        "DOB",
        "college_1",
        "college_2",
        "college_3",
        "college_4",
        "college_5",
        "college_6",
        "college_7",
        "college_8",
        "college_9",
        "college_10",
    ]

    basketball_reference_url = "https://www.basketball-reference.com" 
    base_link = f'{basketball_reference_url}/players'  

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
     
    player_links_by_letter = [f"{base_link}/{letter}/" for letter in alphabet]

    orig_headers = headers.copy()
    for index, header in enumerate(orig_headers):
         headers.insert(2 * index + 1, f"{header}_link")

    data = []

    for letter_inddex, link in enumerate(player_links_by_letter):

        sleep(10)
    
        response = get(link, headers=utils.headers)
        status_code = response.status_code
        
        assert status_code == 200, f"Connection failed with error code {status_code}."

        soup = bs(response.content, 'lxml')
        tags = [list(tag.find_all(["th", "td"]))\
                        for tag in list(soup.find_all("tr"))[1:]]

        for tag in tags:

            data_set = []
            
            for index, header in enumerate(tag):

                text = header.getText()

                if index == 0:
                    player_id = header.attrs["data-append-csv"]
                    data_set.append(player_id)
                    link = ""
                    data_set.append(link)
                
                text = header.getText()

                if header.find("a"):
                    link = header.find("a").attrs["href"]
                else:
                    link = ""
                
                if index == 7:
                    colleges = [tag.getText() for tag in header.find_all('a')]

                    links = [tag.attrs["href"] for tag in list(header.find_all("a"))]

                    for college_index in range(10):
                        try:
                            data_set.append(colleges[college_index])
                            data_set.append(links[college_index])
                        except IndexError:
                            data_set.append("")
                            data_set.append("")
                else:
                    data_set.append(text)
                    data_set.append(link)
        
            data.append(data_set)
        
        print(f'DATA COLLECTED ({alphabet[letter_inddex]}) ')

    headers, data = clean_data(data, headers)
        
    return (headers, data)

def get_player_data():

    # shooting data

    with sqlite3.connect('basketball-reference.db') as connection:
        player = utils.database.search(connection, 'player_index', 'player_name_link')
        player_links = [[link[0], f"https://www.basketball-reference.com{link[0]}"] for link in player]

    no_of_requests = 0
    timer_start_time = time()

    def avoid_rate_limit(no_of_requests: int, timer_start_time: float):

        current_time = time()
        timer = timer_start_time - current_time
        max_rate_time = 60
        max_requests_per_min = 18

        no_of_requests += 1

        if no_of_requests >= max_requests_per_min:
            if not max_rate_time - timer < 0:
                sleep(max_rate_time - timer)

            no_of_requests = 0
            timer_start_time = time()
        
        return no_of_requests, timer_start_time

    for link in player_links:

        # load page in browser
        # [1075:1076]
        index = link[0]
        response = get(link[1], headers=utils.headers)

        no_of_requests, timer_start_time = avoid_rate_limit(no_of_requests, timer_start_time)

        status_code = response.status_code
        
        if not status_code == 200:
            break

        # if not 200 break skip to next player / year

        soup = bs(response.content, 'lxml')
        tags = soup.find_all('li', 'full hasmore')
        data_categories = [tag.find('span').getText() for tag in tags]

        indexed_data_categories = enumerate(data_categories)

        for data_category in indexed_data_categories:
            if data_category[1] == 'Shooting':
                shooting_index = data_category[0]
        if not 'shooting_index' in locals():
            continue

        shooting_years = []

        for a_tag in tags[shooting_index].find_all('a'):
            data_set = []
            shooting_data_year = a_tag.getText()
            shooting_data_link = a_tag.attrs["href"]

            data_set.append(shooting_data_year)
            data_set.append(shooting_data_link)

            shooting_years.append(data_set)
        
        shot_chart = pd.DataFrame(columns=['player', 'season', 'link', 'shot_points','shot_type', 'make_miss','x', 'y', 'date', 'regular_playoff', 'home_away','team_against', 'quater', 'time_left', 'distance', 'lead_swing', 'team_winning', 'score'])

        for year in shooting_years:

            name, url = year

            full_url = f"https://www.basketball-reference.com{url}"

            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
            print(full_url)
            try:
                driver.get(full_url)
                no_of_requests, timer_start_time = avoid_rate_limit(no_of_requests, timer_start_time)
            except WebDriverException:
                no_of_requests, timer_start_time = avoid_rate_limit(no_of_requests, timer_start_time)
                continue

            soup = bs(driver.page_source, 'lxml')
            driver.quit()
            tags = soup.find('div', {'class': 'shot-area'})
            shot_chart_tags = tags.find_all('div')

            for shot in shot_chart_tags:

                shot_position = str(shot.attrs["style"])
                shot_position = shot_position.split('px;')
                x = int(shot_position[0][4:])
                y = int(shot_position[1][5:])

                if shot.getText() == "●":
                    make = 1
                else:
                    make = 0
                
                description_attr = shot.attrs["tip"]
                items = description_attr.split("<br>")

                # Get the date
                date = str(items[0])
                year = date.split(", ")[1]
                day_month = date.split(", ")[0]
                month, day = day_month.split(" ")
                date_str = f"{day}/{month}/{year}"
                date = datetime.strptime(date_str, "%d/%b/%Y")

                # get the team against
                teams_str = str(items[0]).split(", ")[2]
                team_against = teams_str.split(" ")[2]
                if "vs" in teams_str.split(" ")[1]:
                    home_away = 1
                else:
                    home_away = 0

                # get game time
                quater = str(items[1][0])
                game_time = str(items[1])
                game_time_split = game_time.split(" ")
                if "OT" in game_time_split[1]:
                    quater = "OT"

                time_left_str = str(items[1]).split(", ")[1]
                time_left_str = time_left_str.split(" ")[0]
                try:
                    time_left = datetime.strptime(time_left_str, "%M:%S").time()
                except:
                    time_left = datetime.strptime(time_left_str, "%M:%S.%f").time()

                # get shot type
                shot_type_str = str(items[2])
                shot_points = shot_type_str.split(" ")[1][0]
                distance = shot_type_str.split(" ")[3]

                # get score informattion
                score_info = str(items[3])

                if "now" in score_info:
                    lead_swing = True
                else:
                    lead_swing = False
                
                score_type = ""
                if "trails" in score_info:
                    score_type = -1
                elif "leads" in score_info:
                    score_type = 1
                else:
                    score_type = 0

                score = score_info.split(" ")[-1]

                # must reload page for these values

                # shot type


                shot_data = {
                    'player': [index],
                    'season': [name],
                    'link': [url],
                    'shot_points': [shot_points],
                    'shot_type': ['N/A'],
                    'make_miss': [make],
                    'x': [x],
                    'y': [y],
                    'date': [date],
                    'regular_playoff': ['N/A'],
                    'home_away': [home_away],
                    'team_against': [team_against],
                    'quater': [quater],
                    'time_left': [time_left],
                    'distance': [distance],
                    'lead_swing': [lead_swing],
                    'team_winning': [score_type],
                    'score': [score]
                }

                shot_data = pd.DataFrame(shot_data, columns=['player', 'season', 'link', 'shot_points','shot_type', 'make_miss','x', 'y', 'date', 'regular_playoff', 'home_away','team_against', 'quater', 'time_left', 'distance', 'lead_swing', 'team_winning', 'score'],)

                shot_chart = pd.concat([shot_chart, shot_data], ignore_index = True)

        print(f"finished {index}")

    with sqlite3.connect('basketball-reference.db') as connection:
        cursor = connection.cursor()
        shot_chart.to_sql('shot_data', cursor, shot_chart, index=False,)



# fix database entry
# fix abernto01 


