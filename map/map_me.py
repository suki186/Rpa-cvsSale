import geocoder

def get_current_coords():
    try:
        g = geocoder.ip('me')
        return g.latlng  # [위도, 경도]
    except Exception as e:
        print(f"현재 위치 확인 실패: {e}")
        return None, None
