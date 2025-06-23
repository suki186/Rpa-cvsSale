from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

'''
CU의 모든 행사상품을 크롤링하는 함수
크롤링 항목: 편의점, 상품명, 가격, 행사종류, 이미지
'''
def crawl_cu():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # 크롤링 할 CU 홈페이지 URL
    url = "https://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N"
    driver.get(url)
    time.sleep(2)

    product_list = [] # 모든 행사상품 목록
    seen_names = set() # 중복 방지용 집합

    # 행사 종류 매핑
    event_map = {
        "plus1": "1+1",
        "plus2": "2+1"
    }

    page = 1
    prev_count = 0  # 이전 상품 수 기록

    while True:
        #print(f"{page}페이지) 현재 상품 수: {len(seen_names)}")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.select("li.prod_list")

        for item in items:
            try:
                # 상품명
                name_tag = item.select_one("div.name")
                if not name_tag:
                    continue
                name = name_tag.text.strip()

                # 상품명 기준 중복 제거
                if name in seen_names:
                    continue
                seen_names.add(name)

                # 가격
                price_tag = item.select_one("div.price")
                price = ''.join(filter(str.isdigit, price_tag.text.strip())) if price_tag else "0"

                # 이미지
                img_tag = item.select_one("div.prod_img img")
                img_url = img_tag["src"]
                if img_url.startswith("/"):
                    img_url = "https:" + img_url

                # 행사종류
                badge = item.select_one("div.badge span")
                event_class = badge["class"][0] if badge else "none"
                event_type = event_map.get(event_class, "없음")

                # 배열에 추가
                product_list.append({
                    "편의점": "CU",
                    "상품명": name,
                    "가격": price,
                    "행사종류": event_type,
                    "이미지": img_url
                })

            except Exception as e:
                continue

        # 더보기 클릭(10개 마다)
        if len(seen_names) - prev_count >= 10:
            prev_count = len(seen_names)
            try:
                more_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.prodListBtn-w"))
                )
                more_btn.click()
                page += 1
                time.sleep(2)
            except Exception as e:
                break
        else:
            print("마지막 페이지 도달")
            break

    driver.quit()
    return product_list

