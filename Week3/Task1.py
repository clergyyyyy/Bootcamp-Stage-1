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

data_list_2 = data_json_2["data"]
data_list_1 = data_json_1["data"]
data_list_1_layer2 = data_list_1["results"]

data_2_mapping = []
pattern_dist = r"臺北市\s*([\u4e00-\u9fa5]{2,3}區)"
for item in data_list_2:
    station = item.get("MRT", "").strip()
    address = item.get("address", "").strip()

    match = re.search(pattern_dist, address)
    district = match.group(1) if match else "未知區"
    data_2_mapping.append({
        "MRT": station,
        "District": district
    })

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

output_file_spot = "spot.csv"
with open(output_file_spot, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["SpotTitle", "District", "Longitude", "Latitude", "ImageURL"])
    writer.writeheader()
    writer.writerows(final_results)
print(f"CSV output complete: {output_file_spot}")

mrt_dict = {}
for item in data_list_1_layer2:
    attraction_title = item.get("stitle", "").strip()
    info = item.get("info", "").strip()

    mrt_station = None
    for mapping in data_2_mapping:
        station = mapping["MRT"]
        if station and station in info:
            mrt_station = station
            break

    if not mrt_station:
        mrt_station = "None"

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
