import requests

BASE_URL = "https://www.ifixit.com/api/2.0"

def search_device(query: str):
    url = f"{BASE_URL}/search/{query}"
    return requests.get(url, params={"filter": "device"}).json()

def list_guides(device_title: str):
    url = f"{BASE_URL}/wikis/CATEGORY/{device_title}"
    return requests.get(url).json()

def get_guide(guide_id: int):
    url = f"{BASE_URL}/guides/{guide_id}"
    return requests.get(url).json()
