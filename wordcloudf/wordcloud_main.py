# wordcloud_main.py

from .get_keyword import preprocess_keywords
from .keyword_clustering import cluster_similar_keywords, get_top_keywords

def generate_wordcloud_data(gs_file: str, cu_file: str, font_path: str, top_n: int = 30):
    """
    GS25와 CU의 상품명을 분석하여 워드클라우드용 키워드 데이터를 생성합니다.

    Args:
        gs_file (str): GS25 행사상품 CSV 파일 경로
        cu_file (str): CU 행사상품 CSV 파일 경로
        font_path (str): 워드클라우드용 폰트 파일 경로
        top_n (int): 추출할 상위 키워드 개수 (기본 30개)

    Returns:
        Tuple[dict, dict]: (GS25 키워드 딕셔너리, CU 키워드 딕셔너리)
    """

    # 전처리: 불용어 제거 및 명사 추출
    gs25_keywords = preprocess_keywords(gs_file)
    cu_keywords = preprocess_keywords(cu_file)

    # 유사 키워드 군집화
    gs25_clustered = cluster_similar_keywords(gs25_keywords, threshold=85)
    cu_clustered = cluster_similar_keywords(cu_keywords, threshold=85)

    # 상위 키워드 추출
    gs25_top = get_top_keywords(gs25_clustered, top_n=top_n)
    cu_top = get_top_keywords(cu_clustered, top_n=top_n)

    return gs25_top, cu_top
