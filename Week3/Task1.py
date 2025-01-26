import sys
import json
import csv
import re
import urllib.request
import urllib.error
from socket import timeout as SocketTimeout

def extract_first_jpg(filelist):
    urls = re.findall(r"https?://[^\s]+?\.(?:jpg|JPG)", filelist)
    if urls:
        return urls[0]
    else:
        return None

url1 = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1'
url2 = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2'

# 1. 讀取兩個 JSON
try:
    with urllib.request.urlopen(url1, timeout=5) as response1:
        data_json_1 = json.loads(response1.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTP error when fetching url1: {e}")
    sys.exit(1)
except urllib.error.URLError as e:
    if isinstance(e.reason, SocketTimeout):
        print("Timeout occurred when fetching url1. Please try again later or increase the timeout value.")
    else:
        print("Connection error when fetching url1. Check your network or the server status.")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred when fetching url1: {e}")
    sys.exit(1)

try:
    with urllib.request.urlopen(url2, timeout=5) as response2:
        data_json_2 = json.loads(response2.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTP error when fetching url2: {e}")
    sys.exit(1)
except urllib.error.URLError as e:
    if isinstance(e.reason, SocketTimeout):
        print("Timeout occurred when fetching url2. Please try again later or increase the timeout value.")
    else:
        print("Connection error when fetching url2. Check your network or the server status.")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred when fetching url2: {e}")
    sys.exit(1)

print("Both requests completed successfully.")

# 2. 取得資料清單
data_list_2 = data_json_2["data"]
data_list_1 = data_json_1["data"]
data_list_1_layer2 = data_list_1["results"]

# -----------------------------
# 3. 以 SERIAL_NO 為 key 的字典
# -----------------------------
data_2_mapping = {}  # <--- 改成字典
pattern_dist = r"臺北市\s*([\u4e00-\u9fa5]{2,3}區)"

for item in data_list_2:
    s_no = item.get("SERIAL_NO", "").strip()  # <--- 取出 SERIAL_NO
    station = item.get("MRT", "").strip()
    address = item.get("address", "").strip()

    match = re.search(pattern_dist, address)
    district = match.group(1) if match else "未知區"

    # 放進 dict
    data_2_mapping[s_no] = {
        "MRT": station,
        "District": district
    }

# 4. 產生 spot.csv 的內容
final_results = []
for item in data_list_1_layer2:
    attraction_title = item.get("stitle", "").strip()
    info = item.get("info", "").strip()
    longitude = item.get("longitude", "").strip()
    latitude = item.get("latitude", "").strip()
    filelist = item.get("filelist", "").strip()
    image_url = extract_first_jpg(filelist) if filelist else None

    # 新增：透過 SERIAL_NO 去 mapping
    s_no = item.get("SERIAL_NO", "").strip()
    mrt_station = "None"
    district = "None"

    if s_no in data_2_mapping:
        mrt_station = data_2_mapping[s_no]["MRT"]
        district = data_2_mapping[s_no]["District"]

        # 如果官方地址有明顯錯誤，可在這裡做特例手動修正
        # if s_no == "2011051800000057":  # 陽明山溫泉區
        #     district = "士林區"  # 視需求手動更正

    final_results.append({
        "SpotTitle": attraction_title,
        "District": district,
        "Longitude": longitude,
        "Latitude": latitude,
        "ImageURL": image_url if image_url else "None"
    })

output_file_spot = "spot.csv"
with open(output_file_spot, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["SpotTitle", "District", "Longitude", "Latitude", "ImageURL"])
    writer.writeheader()
    writer.writerows(final_results)
print(f"CSV output complete: {output_file_spot}")

# 5. 產出 mrt.csv
mrt_dict = {}
for item in data_list_1_layer2:
    attraction_title = item.get("stitle", "").strip()
    # info = item.get("info", "").strip()   # <--- 不再用 info 來對應

    s_no = item.get("SERIAL_NO", "").strip()
    mrt_station = "None"
    if s_no in data_2_mapping:
        mrt_station = data_2_mapping[s_no]["MRT"]

    if mrt_station not in mrt_dict:
        mrt_dict[mrt_station] = []
    mrt_dict[mrt_station].append(attraction_title)

merged_results = []
for station, titles in mrt_dict.items():
    merged_results.append({
        "MRTStation": station,
        "AttractionTitle": ",".join(titles)
    })

output_file_mrt = "mrt.csv"
with open(output_file_mrt, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["MRTStation", "AttractionTitle"])
    writer.writeheader()
    writer.writerows(merged_results)
print(f"CSV output complete: {output_file_mrt}")
