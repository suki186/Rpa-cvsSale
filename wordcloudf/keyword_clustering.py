# keyword_clustering.py

from collections import Counter
from rapidfuzz import fuzz


def cluster_similar_keywords(keywords, threshold=85):
    """
    유사 키워드를 군집화하고 대표 키워드로 병합
    threshold: 0~100 사이 유사도 기준
    """
    keyword_counts = Counter(keywords)
    clustered = {}

    for word in keyword_counts:
        found = False
        for rep in clustered:
            score = fuzz.ratio(word, rep)
            if score >= threshold:
                clustered[rep] += keyword_counts[word]
                found = True
                break
        if not found:
            clustered[word] = keyword_counts[word]

    return clustered


def get_top_keywords(clustered_dict, top_n=100):
    """빈도 기준 상위 N개 키워드 반환"""
    return dict(sorted(clustered_dict.items(), key=lambda x: x[1], reverse=True)[:top_n])
