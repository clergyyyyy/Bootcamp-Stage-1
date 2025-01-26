import requests
import json
import csv
import re
import sys   # 新增：用來在發生錯誤時退出程式

def extract_first_jpg(filelist):
    urls = re.findall(r"https?://[^\s]+?\.(?:jpg|JPG)", filelist) #選擇第一個.jpg，處理連接下一個/大小寫的情況
    if urls:
        return urls[0]
    else:
        return None

url1 = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1'
url2 = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2'

try:
    response1 = requests.get(url1, timeout=5)
    response1.raise_for_status()
    data_json_1 = json.loads(response1.text)
except requests.exceptions.Timeout:
    print("Timeout occurred when fetching url1. Please try again later or increase the timeout value.")
    sys.exit(1)
except requests.exceptions.ConnectionError:
    print("Connection error when fetching url1. Check your network or the server status.")
    sys.exit(1)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error when fetching url1: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred when fetching url1: {e}")
    sys.exit(1)

try:
    response2 = requests.get(url2, timeout=5)
    response2.raise_for_status()
    data_json_2 = json.loads(response2.text)
except requests.exceptions.Timeout:
    print("Timeout occurred when fetching url2. Please try again later or increase the timeout value.")
    sys.exit(1)
except requests.exceptions.ConnectionError:
    print("Connection error when fetching url2. Check your network or the server status.")
    sys.exit(1)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error when fetching url2: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred when fetching url2: {e}")
    sys.exit(1)

#print(type(data_json_1))  # 應該顯示 <class 'dict'>
#print(type(data_json_2))  # 應該顯示 <class 'dict'>

data_1 = data_json_1
data_2 = data_json_2

mapping_table = {}

data_list_2 = data_json_2["data"]

for item in data_2["data"]:
    attraction_address = item.get("address", '')
    station = item.get("MRT", '')
    address = item.get("address", '')

    #print(f"MRT: {station}, Address: {attraction_address}")


data_list_1 = data_json_1["data"]

data_list_1_layer2 = data_list_1["results"]

for item in data_list_1_layer2:
    info = item.get("info", '')
    attraction_title = item.get("stitle", '')

    #print(f"ATTR NAME: {attraction_title}, INFO: {info[0:10]}")


for item in data_list_1_layer2:
    info = item.get("info", '')
    attraction_title = item.get("stitle", '')

    matched = False
    


#for result in check_pattern_results:
#    print(f"[{result['Case']}] ATTR NAME: {result['ATTR_NAME']}, MRT(parsed): {result['INFO']}") #print all pattern交集

mrt_mapping = {}
data_2_mapping = []

for item in data_list_2:
    mrt_station = item.get("MRT", "").strip()
    address = item.get("address", "").strip()
    if mrt_station:
        if mrt_station not in mrt_mapping:
            mrt_mapping[mrt_station] = []
        mrt_mapping[mrt_station].append(address)

data_2_mapping = []

pattern_dist = r"臺北市\s*([\u4e00-\u9fa5]{2,3}區)"

for item in data_2["data"]:
    station = item.get("MRT", "").strip()
    address = item.get("address", "").strip()

    match = re.search(pattern_dist, address)
    district = match.group(1) if match else "未知區"

    data_2_mapping.append({
        "MRT": station,
        "District": district
    })

#print("MRT/District Mapping")
#for mapping in data_2_mapping:
#    print(f"MRT: {mapping['MRT']}, District: {mapping['District']}")

merged_results = []
for attraction in data_list_1_layer2:
    attraction_title = attraction.get("stitle", "").strip()
    info = attraction.get("info", "").strip()
    mrt_station = None

    for station in mrt_mapping.keys():
        if station in info:
            mrt_station = station
            break

    merged_results.append({
        "MRTStation": mrt_station if mrt_station else "None",
        "AttractionTitle": attraction_title
    })

output_file = "spot.csv"
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["MRTStation", "AttractionTitle"])
    writer.writeheader()
    writer.writerows(merged_results)


final_results = []

for item in data_list_1_layer2:
    attraction_title = item.get("stitle", "").strip()
    info = item.get("info", "").strip()
    longitude = item.get("longitude", "").strip()
    latitude = item.get("latitude", "").strip()
    filelist = item.get("filelist", "").strip()
    image_url = extract_first_jpg(filelist) if filelist else None

    mrt_station = None
    district = "None"

    for mapping in data_2_mapping:
        station = mapping["MRT"]
        if station and station in info:
            mrt_station = station
            district = mapping["District"]
            break

    final_results.append({
        "SpotTitle": attraction_title,
        "District": district,
        "Longitude": longitude,
        "Latitude": latitude,
        "ImageURL": image_url if image_url else "None"
    })

#print("Final Results:")
#for row in final_results:
#    print(row)

output_file = "mrt.csv"
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["MRTStation", "AttractionTitle"])
    writer.writeheader()
    writer.writerows(merged_results)

print(f"CSV output complete:{output_file}")

output_file = "spot.csv"
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["SpotTitle", "District", "Longitude", "Latitude", "ImageURL"])
    writer.writeheader()
    writer.writerows(final_results)

print(f"CSV output complete:{output_file}")
