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



def create_basketball_reference_db(db_name: str = "basketball-reference.db"):

    # Connect to the database (this will create the database if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Close the connection
    conn.close()

def create_player_index_table(db_name: str = "basketball-reference.db"):

    # Connect to the database
    conn = sqlite3.connect(db_name)

    # Create a cursor object
    cursor = conn.cursor()

    # Execute the SQL command to create the table
    cursor.execute('''
        CREATE TABLE champions (
        player_id TEXT PRIMARY KEY,
        player_name TEXT,
        career_start TEXT,
        career_end TEXT,
        position TEXT,
        height TEXT,
        weight TEXT,
        DOB TEXT,
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

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

def get_player_index_data() -> pd.DataFrame:

    headers = [
        "player_id",
        "player_name",
        "career_start",
        "career_end",
        "position",
        "height",
        "weight",
        "DOB",
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

    player_index_df = pd.DataFrame(columns=headers, data=data)
        
    return player_index_df


def create_shot_data_table(db_name: str = "basketball-reference.db"):

    # Connect to the database
    conn = sqlite3.connect('basketball-reference.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Execute the SQL command to create the table
    cursor.execute('''
        CREATE TABLE champions (
        player_id INTEGER PRIMARY KEY,
        season TEXT,
        shot_points INTEGER,
        shot_type TEXT,
        make_miss INTEGER,
        x INTEGER,
        y INTEGER,
        date TEXT,
        regular_playoff INTEGER,
        home_away INTEGER,
        team_against TEXT,
        quater INTEGER,
        time_left TEXT,
        distance TEXT,
        lead_swing INTEGER,
        team_winning INTEGER,
        score TEXT,
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_shot_data_by_player():
    ...



