import os
import requests
import json

TOKEN_FILE = 'kakao_token.json'

def get_access_token():
    # 파일에서 access_token을 불러오기
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            token_data = json.load(f)
            return token_data['access_token']
    
    # 처음 실행할 때만 인증 코드로 access_token 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': '카카오api key',
        'redirect_uri': 'https://localhost.com',
        'code': '인가코드'
    }

    token_response = requests.post(token_url, data=token_data)
    if token_response.status_code != 200:
        print("❌ 인증 실패: ", token_response.json())
        return None
    
    tokens = token_response.json()
    
    # 토큰 저장
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)

    return tokens['access_token']
