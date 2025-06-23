import pandas as pd

def search_product(keyword: str, gs25_df: pd.DataFrame, cu_df: pd.DataFrame):
    gs25_result = gs25_df[gs25_df['상품명'].str.contains(keyword, case=False, na=False)]
    cu_result = cu_df[cu_df['상품명'].str.contains(keyword, case=False, na=False)]
    
    return gs25_result, cu_result
