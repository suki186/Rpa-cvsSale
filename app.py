import streamlit as st
import pandas as pd
st.set_page_config(page_title="편의점 행사상품 서비스", layout="wide")

#from main import generate_wordcloud_data
#from visualize_comparison import visualize_wordclouds_comparison
#import matplotlib.pyplot as plt
from map.map_view import generate_store_map
from product_search import search_product
from streamlit_folium import folium_static
from wordcloudf.wordcloud_main import generate_wordcloud_data
from wordcloudf.visualize_comparison import visualize_wordclouds_comparison
from kakao.send_message import message

# 배경색 변경 (전체 배경색 및 본문 박스 제거)
st.markdown("""
    <style>
        body {
            background-color: #f6f6f6;
        }
        .stApp {
            background-color: #f6f6f6;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------
# 기본 설정
# ------------------
gs_df = pd.read_csv("data/gs25_products.csv")
gs_df = gs_df[gs_df['행사종류'] != "덤증정"]  # 덤증정 제외
cu_df = pd.read_csv("data/cu_products.csv")
FONT_PATH = 'assets/THELeft.ttf'

# 가격, 인덱스 포맷 함수
def format_price(df):
    df = df.copy()
    df['가격'] = df['가격'].apply(lambda x: f"{int(x):,}원" if str(x).isdigit() else x)
    df.reset_index(drop=True, inplace=True)
    df.index += 1  # 인덱스를 1부터 시작하게
    return df


st.markdown(
    "<h1 style='text-align: center;'>🍙 편의점 상품 뜯어먹기</h1>",
    unsafe_allow_html=True
)

# ------------------
# 네비게이션 탭
# ------------------
tabs = st.tabs(["행사상품 검색", "주변 편의점 & 추천 상품", "행사 키워드 한눈에 보기", "모든 행사상품"])

# ------------------
# 1. 상품 검색 기능
# ------------------
with tabs[0]:
    st.header("🔍 행사상품 검색")
    search_col1, search_col2, _ = st.columns([5, 4, 1])
    with search_col2:
        keyword = st.text_input("", placeholder="상품명을 입력하세요 (띄어쓰기 제외)", key="search_input", label_visibility="collapsed")

    if keyword:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("GS25")
            gs_result, cu_result = search_product(keyword, gs_df, cu_df)
            if not gs_result.empty:
                st.dataframe(format_price(gs_result[['상품명', '가격', '행사종류']]))
            else:
                st.info("GS25: 행사하지 않는 상품입니다.")
        with col2:
            st.subheader("CU")
            if not cu_result.empty:
                st.dataframe(format_price(cu_result[['상품명', '가격', '행사종류']]))
            else:
                st.info("CU: 행사하지 않는 상품입니다.")

# ------------------
# 2. 주변 편의점 지도 표시, 추천 상품 버튼
# ------------------
with tabs[1]:
    st.header("❓ 편의점에서 뭘 살까?")
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("📍 내 주변 편의점 보기"):
            map_obj = generate_store_map(radius=700, size=15, pages=3)
            if map_obj:
                folium_static(map_obj, width=800, height=500)
            else:
                st.error("현재 위치를 확인할 수 없거나 지도 생성에 실패했습니다.")
        else:
            st.info("주변에 있는 편의점을 찾아보세요!")
    with btn_col2:
        if st.button("🎁 추천상품 확인"):
            result = message()
            if result:
                st.success("카카오톡 전송 완료!")
            else:
                st.error("카카오톡 전송 실패..")
        else:
            st.info("카카오톡으로 추천상품이 전송됩니다.")


# ------------------
# 3. 키워드 워드클라우드
# ------------------
with tabs[2]:
    st.header("☁️ 키워드 워드클라우드")
    gs_file = "data/gs25_products.csv"
    cu_file = "data/cu_products.csv"

    gs_top, cu_top = generate_wordcloud_data(gs_file, cu_file, FONT_PATH)
    fig = visualize_wordclouds_comparison(gs_top, cu_top, label1="GS25", label2="CU", font_path=FONT_PATH, return_fig=True)

    st.pyplot(fig)

# ------------------
# 4. 모든 행사상품 조회
# ------------------
with tabs[3]:
    st.header("📊 모든 행사상품 조회")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("GS25")
        gs_event = st.radio("", options=gs_df['행사종류'].unique(), horizontal=True, key="gs_radio")
        filtered_gs = gs_df[gs_df['행사종류'] == gs_event]
        st.dataframe(format_price(filtered_gs[['상품명', '가격']]))

    with col2:
        st.subheader("CU")
        cu_event = st.radio("", options=cu_df['행사종류'].unique(), horizontal=True, key="cu_radio")
        filtered_cu = cu_df[cu_df['행사종류'] == cu_event]
        st.dataframe(format_price(filtered_cu[['상품명', '가격']]))
