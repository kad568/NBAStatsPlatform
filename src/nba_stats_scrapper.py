from requests import get


basketball_reference_url = "https://www.basketball-reference.com/"

def get_nba_seasons(target_url: str = basketball_reference_url, proxies: dict = None) -> list:

    response = get(target_url, proxies=proxies)
    status_code = response.status_code
    
    assert status_code == 200, f"Connection not made. Error code : {status_code}"


if __name__ == "__main__":

    pass