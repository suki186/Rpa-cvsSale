import requests
from config import KAKAO_REST_API_KEY

def address_to_coords(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {"query": address}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return None, None

    result = response.json()
    documents = result.get("documents", [])
    if not documents:
        return None, None

    first_match = documents[0]
    return float(first_match["y"]), float(first_match["x"])
