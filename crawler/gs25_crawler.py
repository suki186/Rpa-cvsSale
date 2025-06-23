from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

'''
GS25의 모든 행사상품을 크롤링 하는 함수
크롤링 목록: 편의점, 상품명, 가격, 행사종류, 이미지
'''
def crawl_gs25():
    options = Options()
    options.add_argument("--headless") # 창 띄우지 않고 실행
    driver = webdriver.Chrome(options=options)

    # 크롤링 할 GS25 홈페이지 URL
    url = "http://gs25.gsretail.com/gscvs/ko/products/event-goods"
    driver.get(url)

    # '전체' 탭 클릭
    driver.find_element(By.ID, "TOTAL").click()
    time.sleep(2)

    product_list = [] # 모든 행사상품 목록
    seen_names = set()  # 중복 방지용 집합

    # 행사 종류 매핑
    event_map = {
        "ONE_TO_ONE": "1+1",
        "TWO_TO_ONE": "2+1",
        "GIFT": "덤증정"
    }

    for page in range(1, 228):
        #print(f"{page}페이지) 현재 상품 수: {len(product_list)}")

        # 페이지 이동
        driver.execute_script(f"goodsPageController.movePage({page})")
        #time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.select("ul.prod_list li")

        for item in items:
            try:
                # 상품명
                name_tag = item.select_one("p.tit")
                if not name_tag:
                    continue
                name = name_tag.text.strip()

                # 상품명 기준 중복 제거
                if name in seen_names:
                    continue
                seen_names.add(name)

                # 가격
                raw_price = item.select_one("span.cost").text.strip()
                price = ''.join(filter(str.isdigit, raw_price))

                # 이미지
                img_tag = item.select_one("p.img img")
                img_url = img_tag["src"]
                if img_url.startswith("/"):
                    img_url = "https://gs25.gsretail.com" + img_url

                # 행사종류
                flag_box = item.select_one("div.flag_box")
                if flag_box:
                    flag_class = flag_box["class"][-1]
                    event_type = event_map.get(flag_class, "기타")
                else:
                    event_type = "없음"

                # 배열에 추가
                product_list.append({
                    "편의점": "GS25",
                    "상품명": name,
                    "가격": price,
                    "행사종류": event_type,
                    "이미지": img_url
                })
            except Exception as e:
                continue

    driver.quit()
    return product_list

