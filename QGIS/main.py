import pandas as pd
import folium
from geopy.geocoders import Nominatim
import time
import osmnx as ox

# Đọc dữ liệu từ file Excel
file_path = "E:\\HK1_2024_2025\\hethongthongtin\\cac_quan_lau.xlsx"  # Đường dẫn tới file Excel
df = pd.read_excel(file_path, engine="openpyxl")

# # Dùng geopy để lấy tọa độ từ địa chỉ
# geolocator = Nominatim(user_agent="geoapiExercises")
#
# # Hàm lấy tọa độ dựa trên địa chỉ
# def get_coordinates(address):
#     try:
#         location = geolocator.geocode(address)
#         time.sleep(1)  # Thêm độ trễ để tránh bị giới hạn truy vấn
#         return location.latitude, location.longitude
#     except:
#         print(f"Không thể lấy tọa độ cho địa chỉ: {address}")
#         return None, None
#
# # Lấy tọa độ cho từng địa chỉ và tạo 2 cột latitude, longitude
# df['latitude'], df['longitude'] = zip(*df['address'].apply(get_coordinates))

# Tạo bản đồ
map_center = [21.0294498, 105.7842894]  # Tọa độ trung tâm quận Cầu Giấy
m = folium.Map(location=map_center, zoom_start=15)

# Thêm ranh giới khu vực Cầu Giấy bằng OSMnx
place_name = "Cầu Giấy, Hà Nội, Vietnam"
boundary = ox.geocode_to_gdf(place_name)  # Tải ranh giới khu vực
geo_json = boundary.geometry.iloc[0].__geo_interface__

# Thêm ranh giới vào bản đồ Folium
folium.GeoJson(
    geo_json,
    name="Ranh giới Cầu Giấy",
    style_function=lambda x: {"color": "blue", "weight": 2, "fillOpacity": 0.1},
).add_to(m)

# Thêm các quán lẩu vào bản đồ
for _, row in df.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        # Tạo nội dung popup với CSS
        popup_html = f"""
               <div style="width: 200px; font-family: Arial, sans-serif;">
                   <h4 style="margin: 0; color: #d9534f;">{row['name']}</h4>
                   <p style="margin: 5px 0; font-size: 14px; color: #5bc0de;">{row['address']}</p>
               </div>
               """
        popup = folium.Popup(popup_html, max_width=250)

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            icon=folium.Icon(color='red', icon='cutlery')
        ).add_to(m)
    else:
        print(f"Không thể thêm quán {row['name']} ({row['address']}) do không có tọa độ.")

# Hiển thị bảng dữ liệu đã xử lý
print(df[['name', 'address', 'latitude', 'longitude']])

# Lưu bản đồ ra file HTML
m.save("lau_map_cau_giay.html")
print("Bản đồ đã được tạo và lưu dưới tên 'lau_map_cau_giay.html'")
