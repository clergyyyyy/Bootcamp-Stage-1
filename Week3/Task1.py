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

#=======【新增Try-Except & 延長timeout】=======#
try:
    response1 = requests.get(url1, timeout=5)  # timeout由1增至5
    response1.raise_for_status()              # 若出現非2xx狀態則丟出HTTPError
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
    response2 = requests.get(url2, timeout=5)  # timeout由1增至5
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
#=======【新增Try-Except & 延長timeout】=======#

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

#Parse Logic
#Case 1: start with 捷運站名： end with 站
#Case 2: start with 捷運 end with 站
#Case 3: start with 捷運動物園 no 站
#Case 4: 沒有寫捷運 但有線至
#Case 5: 沒有寫捷運 但有線
#Case 6: 沒有包含捷運 None
#例外處理：寫死用mapping 表

#捷運車站站名字數不得超過六個字
pattern_1 = r"捷運站名：([\u4e00-\u9fa5]{2,6})站" #中間只保留1-10個捷運站
pattern_2 = r"捷運([\u4e00-\u9fa5]{1,10})站" #中間只保留1-10個捷運站
pattern_3 = r"捷運([\u4e00-\u9fa5]{2,6})" #有捷運 沒有站
pattern_4 = r"線至([\u4e00-\u9fa5]{2,6})站" #沒有寫捷運 但有線至
pattern_5 = r"線([\u4e00-\u9fa5]{2,6})站" #沒有寫捷運 但有線
pattern_new = r"捷運.*線至([\u4e00-\u9fa5]{2,6})站" #有捷運又有限制 #最嚴格 和case1一起判斷
check_pattern_results = []

fixed_mrt_mapping = {
    "臺北市鄉土教育中心(剝皮寮歷史街區)": "龍山寺",
    "北投文物館": "北投",
    "行天宮北投分宮-忠義廟": ["復興崗", "忠義"],  #多站
    "臺北市立美術館": "圓山",
    "台北探索館": "市政府",
    "台北當代藝術館": "中山",
    "陽明山溫泉區": "劍潭",
    "北投圖書館": "新北投",
    "雙溪生活水岸": ["芝山", "士林"],
    "臺北市鄉土教育中心(剝皮寮歷史街區)": "龍山寺",
    "行天宮": "行天宮",
    "新北投溫泉區": "新北投",
}

for item in data_list_1_layer2:
    info = item.get("info", '')
    attraction_title = item.get("stitle", '')

    match_pattern_1 = re.search(pattern_1, info)
    match_pattern_2 = re.search(pattern_2, info)
    match_pattern_3 = re.search(pattern_3, info)
    match_pattern_4 = re.search(pattern_4, info)
    match_pattern_5 = re.search(pattern_5, info)
    match_pattern_new = re.search(pattern_new, info)

    matched = False
    
    if attraction_title in fixed_mrt_mapping:
        MRT_Station = fixed_mrt_mapping[attraction_title]
        check_pattern_results.append({"Case": "Fixed-Mapping", "ATTR_NAME": attraction_title, "INFO": MRT_Station})
        matched = True
    if not matched and match_pattern_1 and match_pattern_new:
        MRT_Station = match_pattern_1.group(1)
        check_pattern_results.append({"Case": "Case 1", "ATTR_NAME": attraction_title, "INFO": MRT_Station})
        matched = True
    elif not matched and match_pattern_2:
        MRT_Station = match_pattern_2.group(1)
        check_pattern_results.append({"Case": "Case 2", "ATTR_NAME": attraction_title, "INFO": MRT_Station})
        matched = True
    elif not matched and match_pattern_3:
        MRT_Station = match_pattern_3.group(1)
        check_pattern_results.append({"Case": "Case 3", "ATTR_NAME": attraction_title, "INFO": MRT_Station})
        matched = True
    elif not matched and match_pattern_4:
        MRT_Station = match_pattern_4.group(1)
        check_pattern_results.append({"Case": "Case 4", "ATTR_NAME": attraction_title, "INFO": MRT_Station})
        matched = True
    elif not matched and match_pattern_5:
        MRT_Station = match_pattern_5.group(1)
        check_pattern_results.append({"Case": "Case 5", "ATTR_NAME": attraction_title, "INFO": MRT_Station})
        matched = True
    elif not matched and "捷運" not in info:
        check_pattern_results.append({"Case": "Case 6", "ATTR_NAME": attraction_title, "INFO": None})
        matched = False

#針對「捷運」還是移除不掉字的case一次性移除
for result in check_pattern_results:
    if result["INFO"]:  #排除none的情況
        if isinstance(result["INFO"], list):  #如果是列表，移除捷運
            result["INFO"] = [station.replace("捷運", "") for station in result["INFO"]]
        elif isinstance(result["INFO"], str):  #如果是字串，直接替換
            result["INFO"] = result["INFO"].replace("捷運", "")

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

output_file = "spot.csv"
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["MRTStation", "AttractionTitle"])
    writer.writeheader()
    writer.writerows(merged_results)

print(f"CSV output complete:{output_file}")

output_file = "final_results.csv"
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["SpotTitle", "District", "Longitude", "Latitude", "ImageURL"])
    writer.writeheader()
    writer.writerows(final_results)

print(f"CSV output complete:{output_file}")
