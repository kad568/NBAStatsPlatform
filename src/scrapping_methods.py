import utils

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


def get_table_data(url: str,headers: list, proxies: dict = None, text_splitter = '\xa0') -> list: 

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

            if text_splitter in text:
                name, stat = utils.split_player_stat(text)
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

def get_player(url: str,headers: list, proxies: dict = None) -> list:

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    basketball_reference_url = "https://www.basketball-reference.com/" 
    base_link = f'{basketball_reference_url}/players'   
    player_links_by_letter = [f"{base_link}/{letter}/" for letter in alphabet]

    
    utils.get_relevant_tags(player_links_by_letter[0])

    return