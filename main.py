import pandas as pd
import folium
from geopy.geocoders import Nominatim
import time
import osmnx as ox

# Đọc dữ liệu từ file Excel
file_path = "./highlands_coffee.xlsx"  # Đường dẫn tới file Excel
df = pd.read_excel(file_path, engine="openpyxl")



# Tạo bản đồ
map_center_caugiay = [21.0294498, 105.7842894]  # Tọa độ trung tâm quận Cầu Giấy
m = folium.Map(location=map_center_caugiay, zoom_start=15)
map_center_bactuliem = [21.07220759279431, 105.76197986685854] # Tọa độ trung tâm quận Bắc Từ Liêm
n = folium.Map(location=map_center_bactuliem, zoom_start=15)
# Thêm ranh giới khu vực Cầu Giấy bằng OSMnx

bactuliem = "Bắc Từ Liêm, Hà Nội, Vietnam"
bactuliem_boundary = ox.geocode_to_gdf(bactuliem)
geo_json_btl = bactuliem_boundary.geometry.iloc[0].__geo_interface__
caugiay = "Cầu Giấy, Hà Nội, Vietnam"
caugiay_boundary = ox.geocode_to_gdf(caugiay)  # Tải ranh giới khu vực
geo_json = caugiay_boundary.geometry.iloc[0].__geo_interface__

# Thêm ranh giới vào bản đồ Folium
caugiay_layer = folium.FeatureGroup(name="Ranh giới Cầu Giấy")
folium.GeoJson(
    geo_json,
    name="Ranh giới Cầu Giấy",
    style_function=lambda x: {"color": "blue", "weight": 2, "fillOpacity": 0.1},
).add_to(caugiay_layer)

bactuliem_layer = folium.FeatureGroup(name="Ranh giới Bắc Từ Liêm")
folium.GeoJson(
    geo_json_btl,
    name="Ranh giới Bắc Từ Liêm",
    style_function=lambda x: {"color": "blue", "weight": 2, "fillOpacity": 0.1},
).add_to(bactuliem_layer)

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
        
        
bactuliem_layer.add_to(m) #Thêm layer vào map
caugiay_layer.add_to(m)
folium.LayerControl().add_to(m) #Tạo control


# Hiển thị bảng dữ liệu đã xử lý
print(df[['name', 'address', 'latitude', 'longitude']])


ten = "highlands_cau_giay.html"
# Lưu bản đồ ra file HTML
m.save(ten)
print(f"Bản đồ đã được tạo và lưu dưới tên '{ten}'")
