import utils


def get_table_data(url: str,headers: list, proxies: dict = None) -> list: 
    
    data = []

    for header in headers:
            data.append([])
            data.append([])

    tags = utils.get_relevant_tags(url)

    for tag in tags:
        for index, header in enumerate(tag):
            
            text = header.getText()

            if header.find("a"):
                link = header.find("a").attrs["href"]
            else:
                 link = ""

            data[2 * index].append(text)
            data[2 * index + 1].append(link)

    orig_headers = headers.copy()
    for index, header in enumerate(orig_headers):
         headers.insert(2 * index + 1, f"{header}_link")

    return (headers, data)