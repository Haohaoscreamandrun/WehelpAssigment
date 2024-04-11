# Task 1
def find_and_print(messages, current_station):

    # your code here
    # declare the sequence of Songshan-Xindian Line and Xiaobitan Line
    green_line = {
        'Songshan': 0,
        'Nanjing Sanmin': 1,
        'Taipei Arena': 2,
        'Nanjing Fuxing': 3,
        'Sonjiang Nanjing': 4,
        'Zhongshan': 5,
        'Beimen': 6,
        'Ximen': 7,
        'Xiaonanmen': 8,
        'Chiang Kai-Shek Memorial Hall': 9,
        'Guting': 10,
        'Taipower Building': 11,
        'Gongguan': 12,
        'Wanlong': 13,
        'Jingmei': 14,
        'Dapinglin': 15,
        'Qizhang': 16,
        'Xindian City Hall': 17,
        'Xindian': 18
    }
    xiaobitan_line = {
        'Qizhang': 0,
        'Xiaobitan': 1
    }
    # take in JSON message and process
    location = {}
    for name, sentence in messages.items():
        # check if sentence includes station
        for station in green_line.keys() | xiaobitan_line.keys():
            if station in sentence:
                # if yes, add to location pairs
                location[name] = station
                break
    # calculate the distance based on currentStation
    distance = {}
    for name, station in location.items():
        if current_station in green_line:
            if station in green_line:
                # cond 1: station on green_line
                distance[name] = abs(green_line[station] - green_line[current_station])
            else:
                # cond 2: station not on green_line, current-Qizhang-station
                distance[name] = abs(green_line['Qizhang'] - green_line[current_station]) + xiaobitan_line[station]
        elif current_station in xiaobitan_line:
            if station in green_line:
                # cond 1: station on green_line, current-Qizhang-station
                distance[name] = xiaobitan_line[current_station] + abs(green_line['Qizhang'] - green_line[station])
            else:
                # cond 2: station not on green_line
                distance[name] = abs(xiaobitan_line[station] - xiaobitan_line[current_station])
    # find the shortest distance and its keys
    shortest_distance = min(distance.values())
    # list comprehension, which is a concise way to create lists in Python. It generates a new list containing the name (key) for each key-value pair in the distance dictionary where the value dis is equal to shortest_distance.
    names = [name for name, dis in distance.items() if dis == shortest_distance]
    
    # print out results
    print(', '.join(names))




messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you."
}
find_and_print(messages, "Wanlong")  # print Mary
find_and_print(messages, "Songshan")  # print Copper
find_and_print(messages, "Qizhang")  # print Leslie
find_and_print(messages, "Ximen")  # print Bob
find_and_print(messages, "Xindian City Hall")  # print Vivian

# Task 2
# your code here, maybe
def book(consultants, hour, duration, criteria):


    # your code here
    consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
    ]


book(consultants, 15, 1, "price")  # Jenny
book(consultants, 11, 2, "price")  # Jenny
book(consultants, 10, 2, "price")  # John
book(consultants, 20, 2, "rate")  # John
book(consultants, 11, 1, "rate")  # Bob
book(consultants, 11, 2, "rate")  # No Service
book(consultants, 14, 3, "price")  # John

# Task 3
def func(*data):
    
    print(*data)
    # your code here


func("彭大牆", "陳王明雅", "吳明")  # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")  # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")  # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆")  # print 夏曼藍波安


# Task 4
def get_number(index):
    
    print(index)
    # your code here


get_number(1)  # print 4
get_number(5)  # print 15
get_number(10)  # print 25
get_number(30)  # print 70

# Task 5
def find(spaces, stat, n):
    # your code here
    print(spaces)

find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2)  # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4)  # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4)  # print 2
