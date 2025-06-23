from map.map_me import get_current_coords
from map.store_fetcher import fetch_convenience_stores, save_stores_to_csv
from map.map_view import show_stores_on_map

def main(radius=700, size=20, pages=3, output_path='map/map.html'): #기본값 설정
    print("📍 현재 위치 확인 중...")
    lat, lng = get_current_coords()

    if lat is None or lng is None:
        print("위치 정보를 가져올 수 없습니다.")
        return

    print(f"현재 위치: 위도 {lat}, 경도 {lng}")

    print(f"반경 {radius}m 내 편의점 목록 가져오는 중 (페이지당 {size}개, 총 {pages}페이지)...")
    stores = fetch_convenience_stores(x=lng, y=lat, radius=radius, size=size, max_pages=pages)
    print(f"편의점 {len(stores)}개 수집 완료")

    print("CSV 저장 중...")
    stores_with_coords = save_stores_to_csv(stores)  # 좌표 포함 리스트 받음

    print("지도 생성 중...")
    show_stores_on_map(stores_with_coords, center_lat=lat, center_lng=lng)

    print("모든 작업 완료!")
    return output_path


