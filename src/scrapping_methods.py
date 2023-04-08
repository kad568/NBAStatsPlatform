import utils
from requests import get
from bs4 import BeautifulSoup as bs
from time import sleep

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