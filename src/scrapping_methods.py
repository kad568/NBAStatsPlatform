import utils
from requests import get
from bs4 import BeautifulSoup as bs
from time import sleep
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


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
        player_links = [f"https://www.basketball-reference.com{link[0]}" for link in utils.database.search(connection, 'player_index', 'player_name_link')]

    for index, link in enumerate(player_links[3:4]):

        # load page in browser

        sleep(3)

        response = get(link, headers=utils.headers)
        status_code = response.status_code
        
        assert status_code == 200, f"Connection failed with error code {status_code}."

        soup = bs(response.content, 'lxml')
        tags = soup.find_all('li', 'full hasmore')
        data_categories = [tag.find('span').getText() for tag in tags]

        indexed_data_categories = enumerate(data_categories)

        for data_category in indexed_data_categories:
            if data_category[1] == 'Shooting':
                shooting_index = data_category[0]

        shooting_years = []


        for a_tag in tags[shooting_index].find_all('a'):
            data_set = []
            shooting_data_year = a_tag.getText()
            shooting_data_link = a_tag.attrs["href"]

            data_set.append(shooting_data_year)
            data_set.append(shooting_data_link)

            shooting_years.append(data_set)
        
        shot_chart = pd.DataFrame(columns=['season', 'link', 'shot_type','make_miss','x', 'y', 'date', 'team_against', 'time_left', 'distance', 'team_winning', 'score'])

        for year in [shooting_years[0]]:

            name, url = year

            full_url = f"https://www.basketball-reference.com{url}"

            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
            driver.get(full_url)

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
                
                date_attr = shot.attrs["tip"]
                items = date_attr.split("<br>")

                date = items[0]

                print(x, y, make)


                shot_data = {
                    'season': name,
                    'link': url,
                    'shot_type': ...,
                    'make_miss': make,
                    'x': x,
                    'y': y,
                    'date': ...,
                    'team_against': ...,
                    'time_left': ...,
                    'distance': ...,
                    'team_winning': ...,
                    'score': ...
                }
                

        # shot_chart = pd.DataFrame(columns=['year', 'link', 'shot_type','make_miss','x', 'y', 'date', 'team_against', 'time_left', 'distance', 'team_winning', 'score'])
            # extraxt all data from each div
            # pandas datafram with each


