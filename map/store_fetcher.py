import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import pandas as pd
from config import KAKAO_REST_API_KEY, STORE_CSV_PATH

from map.map_api import address_to_coords  # 주소 변환 전용 함수


def fetch_convenience_stores(x, y, radius=500, size=15, max_pages=3):
    """
    카카오 로컬 API를 사용해 특정 위치(x, y) 기준 반경 내 편의점 정보를 가져옴.
    CU와 GS25만 필터링해서 반환.
    """
    url = "https://dapi.kakao.com/v2/local/search/category.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    stores = []

    for page in range(1, max_pages + 1):
        params = {
            "category_group_code": "CS2",  # 편의점 카테고리
            "x": x,
            "y": y,
            "radius": radius,
            "size": size,
            "page": page
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"❌ Error fetching page {page}: {response.status_code}")
            break

        data = response.json().get("documents", [])
        if not data:
            break  # 더 이상 데이터 없음

        for store in data:
            name = store["place_name"]
            address = store["address_name"]
            if "CU" in name.upper() or "GS25" in name.upper():
                stores.append((name, address))

    return stores

def save_stores_to_csv(store_list):
    """
    (이름, 주소) 리스트를 위도/경도로 변환하고 CSV로 저장,
    변환된 리스트도 반환함
    """
    rows = []
    for name, address in store_list:
        lat, lon = address_to_coords(address)
        if lat is not None and lon is not None:
            rows.append({
                "편의점명": name,
                "주소": address,
                "위도": lat,
                "경도": lon
            })
            print(f"변환 완료: {name}")
        else:
            print(f"변환 실패: {name}")

    df = pd.DataFrame(rows)
    df.to_csv(STORE_CSV_PATH, index=False, encoding="utf-8-sig")
    print(f"저장 완료: {STORE_CSV_PATH}")

    return rows  # 변환된 리스트 반환

