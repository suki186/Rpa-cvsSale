# preprocessing.py

import pandas as pd
import re
from typing import List, Dict

# 사용자 정의 불용어 목록
STOPWORDS = ['맛', '음료', '제품', '신상품', '행사', '용', '팩', '병', '개']

# 브랜드/제품명 통합을 위한 규칙 사전
MERGE_RULES = {
    r'젤리블리.*': '젤리블리',
    r'초코칩.*': '초코칩',
    r'.*콜라': '콜라',
    r'.*사이다': '사이다',
    r'.*캔디': '캔디',
    r'.*티라미수.*': '티라미수'
}

def clean_text(text: str) -> str:
    """소문자화, 특수문자 제거 등 기본 정제"""
    text = text.lower()
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', text)
    return text

def tokenize_and_filter(product_names: List[str]) -> List[str]:
    """상품명에서 키워드 추출 및 불용어 제거"""
    keywords = []
    for name in product_names:
        name = clean_text(name)
        tokens = name.split()
        for token in tokens:
            if all(sw not in token for sw in STOPWORDS):
                keywords.append(token)
    return keywords

def apply_merge_rules(keywords: List[str]) -> List[str]:
    """정규표현식 기반 키워드 통합"""
    merged = []
    for word in keywords:
        replaced = False
        for pattern, replacement in MERGE_RULES.items():
            if re.fullmatch(pattern, word):
                merged.append(replacement)
                replaced = True
                break
        if not replaced:
            merged.append(word)
    return merged

def preprocess_keywords(filepath: str) -> List[str]:
    """CSV 파일에서 상품명을 읽어 키워드 리스트 반환"""
    df = pd.read_csv(filepath)
    if '상품명' not in df.columns:
        raise ValueError("CSV 파일에 '상품명'이 존재하지 않습니다.")
    product_names = df['상품명'].dropna().tolist()
    keywords = tokenize_and_filter(product_names)
    merged_keywords = apply_merge_rules(keywords)
    return merged_keywords
