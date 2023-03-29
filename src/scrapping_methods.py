import utils


def get_table_data(url: str,headers: list, proxies: dict = None) -> list: 
    
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

            data_set.append(text)
            data_set.append(link)

        data.append(tuple(data_set))

    # adjust original header
    orig_headers = headers.copy()
    for index, header in enumerate(orig_headers):
         headers.insert(2 * index + 1, f"{header}_link")

    return (headers, data)