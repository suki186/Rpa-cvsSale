# data_parser.py

import pandas as pd
import os

# 크롤링 함수 불러오기
from crawler.gs25_crawler import crawl_gs25
from crawler.cu_crawler import crawl_cu

def save_to_csv(data, filename):
    """
    상품 데이터를 CSV 파일로 저장
    GS25 -> gs25_producs.csv   |   CU -> cu_producs.csv
    """
    os.makedirs("../data", exist_ok=True)  # 폴더 없으면 생성
    df = pd.DataFrame(data)
    df.to_csv(f"../data/{filename}", index=False, encoding="utf-8-sig")
    print(f"{filename} 저장 완료 ({len(df)}개 항목)")

def main():
    # GS25 크롤링 및 저장
    print("▶ GS25 행사상품 크롤링 시작")
    try:
        gs25_data = crawl_gs25()
    except Exception as e:
        print(f"GS25 크롤링 오류: {e}")
    save_to_csv(gs25_data, "gs25_products.csv")

    # CU 크롤링 및 저장
    print("▶ CU 행사상품 크롤링 시작")
    try:
        cu_data = crawl_cu()
    except Exception as e:
        print(f"CU 크롤링 오류: {e}")
    save_to_csv(cu_data, "cu_products.csv")

if __name__ == "__main__":
    main()
