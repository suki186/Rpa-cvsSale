import requests
import json
import csv
import random
from kakao.kakaotalk import get_access_token
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '../data'))

def load_random_items(filename, count=2):
    csv_path = os.path.join(DATA_DIR, filename)
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=',')
        items = list(reader)
        return random.sample(items, count)

def message():
    access_token = get_access_token()
    if not access_token:
        print("❌ access_token 없음. 메시지 전송 실패")
        return

    # 편의점별 2개씩 상품 뽑기
    cu_items = load_random_items('cu_products.csv', 1)
    gs_items = load_random_items('gs25_products.csv', 1)
    selected_items = cu_items + gs_items

    # 메시지 텍스트 만들기
    description = ""
    for item in selected_items:
        store = item["편의점"].strip()
        name = item["상품명"].strip()
        price = item["가격"].strip()
        description += f"🔸 {store}: {name} {price}원\n"

    # 대표 이미지로 첫 번째 상품 이미지 사용
    image_url = selected_items[0]["이미지"].strip()

    message_data = {
        "template_object": json.dumps({
            "object_type": "feed",
            "content": {
                "title": "🛒 오늘의 추천 상품",
                "description": description.strip(),
                "image_url": image_url,
                "image_width": 640,
                "image_height": 640,
                "link": {
                    "web_url": "http://gs25.gsretail.com/gscvs/ko/products/event-goods",
                    "mobile_web_url": "http://gs25.gsretail.com/gscvs/ko/products/event-goods"
                }
            },
            "buttons": [
                {
                    "title": "자세히 보기",
                    "link": {
                        "web_url": "https://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N",
                        "mobile_web_url": "https://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N"
                    }
                }
            ]
        })
    }

    send_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.post(send_url, headers=headers, data=message_data)

    if response.status_code != 200:
        print("❌ 메시지 전송 실패: ", response.json())
        return False
    else:
        print("✅ 메시지 전송 성공!")
        return True
   