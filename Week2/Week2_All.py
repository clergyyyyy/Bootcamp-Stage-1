import re
print("===Task 1===")
def find_and_print(messages, current_station):

    cleaned_messages = {key: re.sub(r'[^\w\s]', '', value) for key, value in messages.items()}
    # print(cleaned_messages)
    split_messages = {key: value.split() for key, value in cleaned_messages.items()}
    # print(split_messages)

    for key, words in split_messages.items():
        for word in words:
            if word in line_1_station:
                friend_station_index[key] = line_1_station.index(word)
                break
            elif word in line_2_station:
                friend_station_index[key] = -1  #-1表示在 line_2
                break
    
    # 用current_station的值找list的index
    current_station_index = line_1_station.index(current_station)
    print(f"Current station: ", current_station, " Index: ", current_station_index)
    for key, value in friend_station_index.items():
        target_index = friend_station_index.get(key)
        if target_index > 0 or target_index == 0:
            record_distance[key] = abs(target_index - current_station_index)
        elif target_index < 0: #target station在line 2
            record_distance[key] = abs(16 - current_station_index) + 1
    result = min(record_distance, key=record_distance.get)
    print(f"Nearest friend: {result}, distance: {record_distance[result]}")

    return result

messages={
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you.",
}

record_distance={
    "Leslie": 0,
    "Bob": 0,
    "Mary": 0,
    "Copper": 0,
    "Vivian": 0,
}

friend_station_index={
    "Leslie": 0,
    "Bob": 0,
    "Mary": 0,
    "Copper": 0,
    "Vivian": 0,
}

# 用list存儲站名，index為其編號
line_1_station = ["Songshan", "Nanjing Sanmin", "Arena", "Nanjing Fuxing", "Songjiang Nanjing", "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", "Chiang Kai-Shek Memorial Hall", "Guting", "Taipower Building", "Gongguan", "Wanlong", "Jingmei", "Dapingling", "Qizhang", "Xindian City Hall", "Xindian"]
line_2_station = ["Qizhang", "Xiaobitan"]


find_and_print(messages, "Wanlong")
find_and_print(messages, "Songshan")
find_and_print(messages, "Qizhang")
find_and_print(messages, "Ximen")
find_and_print(messages, "Xindian City Hall")

print("===Task 2===")
booked_slots = {
    "John": [],
    "Bob": [],
    "Jenny": []
}

consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3.0, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800},
]

def book(consultants, hour, duration, criteria):
    global booked_slots #改成通用
    end_time = hour + duration
    request_time = (hour, end_time)
    
    available_consultants = []
    
    for consultant in consultants:
        name = consultant['name']
        available_status = True
        for slot in booked_slots.get(name, []):
            booked_start, booked_end = slot
            if not (end_time <= booked_start or hour >= booked_end):
                available_status = False
                break
        if available_status:
            available_consultants.append(consultant)
    
    if not available_consultants:
        print("No Service")
        return "No Service"
    
    if criteria == "price":
        selected = min(available_consultants, key=lambda x: x['price'])
    elif criteria == "rate":
        selected = max(available_consultants, key=lambda x: x['rate'])
    else:
        print("Error! Wrong criteria.")
        return "Error! Wrong criteria."
    
    booked_slots[selected['name']].append(request_time)
    
    print(f"Consultant: {selected['name']}. Booked successfully!")
    return selected['name']

print(book(consultants, 15, 1, "price"))  #Jenny 
print(book(consultants, 11, 2, "price"))  #Jenny 
print(book(consultants, 10, 2, "price"))  #John 
print(book(consultants, 20, 2, "rate"))   #John 
print(book(consultants, 11, 1, "rate"))   #Bob 
print(book(consultants, 11, 2, "rate"))   #No Service 
print(book(consultants, 14, 3, "price"))  #John


print("===Task 3===")
def func(*data):
    result=[]
    middle_list = list()
    duplicate_middle_set = set()
    map_table = {}
    for fullname in data:
        name_length = len(fullname)
        if name_length == 1:
            middlename = None
            print("Full name is too short")
            continue
        elif name_length == 2 or name_length == 3:
            middlename = fullname[1]
            middle_list.append(middlename)
        elif name_length > 3:
            middlename = fullname[2]
            middle_list.append(middlename)
        else:
            print("Full name is too long")
            continue


        if middlename in map_table:
            map_table[middlename].add(fullname)
            duplicate_middle_set.add(middlename)  #重複的加入duplicate_middle_set
        else:
            map_table[middlename] = {fullname}

    result = set(middle_list) - duplicate_middle_set
    unique_middle_names = [name for name in set(middle_list) if middle_list.count(name) == 1]

    if not unique_middle_names:
        print("No unique middle name!")
        return
    else:
        for unique_name in unique_middle_names:
            print(f"唯一Middle name: {unique_name}, 全名: {map_table[unique_name]}")

func("彭大牆","陳王明雅","吳明") #彭大牆
func("郭靜雅","王立強","郭林靜宜","郭立恆","林花花") #林花花
func("郭宣雅","林靜宜","郭宣恆","林靜花") #沒有
func("郭宣雅","夏曼藍波安","郭宣恆") #夏曼藍波安


print("===Task 4===")
def get_number(index): 
    extra = 0
    quotient, remainder = divmod(index, 3)
    if remainder == 1:
        extra = 4
    elif remainder == 2:
        extra = 8
    else:
        extra = 0

    total = quotient * 7 + extra
    return total

print(get_number(1))  #4
print(get_number(5))  #15
print(get_number(10)) #25
print(get_number(30)) #70
