from .map_me import get_current_coords
from .store_fetcher import fetch_convenience_stores, save_stores_to_csv
import folium

def generate_store_map(radius=700, size=20, pages=3):
    lat, lng = get_current_coords()
    if lat is None or lng is None:
        return None

    stores = fetch_convenience_stores(x=lng, y=lat, radius=radius, size=size, max_pages=pages)
    stores_with_coords = save_stores_to_csv(stores)

    m = folium.Map(location=[lat, lng], zoom_start=16)
    for store in stores_with_coords:
        name = store["편의점명"]
        s_lat = store["위도"]
        s_lng = store["경도"]
        color = "blue" if "GS25" in name else "purple" if "CU" in name else "gray"

        folium.Marker(
            location=[s_lat, s_lng],
            popup=f'{name}\n{store["주소"]}',
            icon=folium.Icon(color=color, icon='shopping-cart')
        ).add_to(m)

    return m
