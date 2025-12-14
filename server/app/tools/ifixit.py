import requests
from urllib.parse import quote

BASE_URL = "https://www.ifixit.com/api/2.0"


def search_device(query: str) -> dict | None:
    """Return the first matching device from iFixit search."""
    
    query = query.lower().strip()
    for word in ["i want to repair", "please", "my", "broken", "help"]:
        query = query.replace(word, "")
    query = " ".join(query.split())

    url = f"{BASE_URL}/search/{quote(query)}"
    res = requests.get(url, params={"filter": "device"}, timeout=10)
    res.raise_for_status()

    data = res.json()
    results = data.get("matches") or data.get("results") or []
    if not results:
        return None

    return results[0]



def list_guides(device_title: str) -> list[dict]:
    """Return a list of guides for a given device title."""
    url = f"{BASE_URL}/wikis/CATEGORY/{quote(device_title)}"
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()

    guides = []
    for category_guides in data.values():
        if isinstance(category_guides, list):
            guides.extend(category_guides)
    return guides  


def get_guide(guide_id: int) -> dict:
    url = f"{BASE_URL}/guides/{guide_id}"
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    return res.json()
