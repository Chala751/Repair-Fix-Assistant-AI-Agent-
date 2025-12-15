import requests
from urllib.parse import quote

BASE_URL = "https://www.ifixit.com/api/2.0"
TIMEOUT = 10

def search_device(query: str) -> dict | None:
    url = f"{BASE_URL}/search/{quote(query)}"
    res = requests.get(url, timeout=TIMEOUT)
    res.raise_for_status()

    data = res.json()
    results = data.get("matches") or data.get("results") or []

    # ✅ ONLY accept real devices
    for r in results:
        if r.get("type") == "device":
            return r

    return None

def list_guides(device_name: str) -> list[dict]:
    """
    Uses CATEGORY endpoint.
    device_name MUST be 'iPhone_12'
    """
    device_slug = device_name.replace(" ", "_")

    url = f"{BASE_URL}/wikis/CATEGORY/{quote(device_slug)}"
    res = requests.get(url, timeout=TIMEOUT)
    res.raise_for_status()

    data = res.json()
    guides = []

    for v in data.values():
        if isinstance(v, list):
            guides.extend(v)

    return guides


def get_guide(guide_id: int) -> dict:
    url = f"{BASE_URL}/guides/{guide_id}"
    res = requests.get(url, timeout=TIMEOUT)
    res.raise_for_status()
    return res.json()
