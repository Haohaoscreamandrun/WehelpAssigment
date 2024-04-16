import time
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
                distance[name] = abs(
                    green_line[station] - green_line[current_station])
            else:
                # cond 2: station not on green_line, current-Qizhang-station
                distance[name] = abs(
                    green_line['Qizhang'] - green_line[current_station]) + xiaobitan_line[station]
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
start = time.time()
find_and_print(messages, "Wanlong")  # print Mary
find_and_print(messages, "Songshan")  # print Copper
find_and_print(messages, "Qizhang")  # print Leslie
find_and_print(messages, "Ximen")  # print Bob
find_and_print(messages, "Xindian City Hall")  # print Vivian
end = time.time()
print(end - start)
# Task 2
# your code here, maybe


def book(consultants, hour, duration, criteria):
    # your code here
    # sort data
    status = []
    for consultant in consultants:
        status.append(list(consultant.values()))
    # confirmation of time slot
    # inquired time
    inquire_time = []
    for i in range(1, duration + 1):
        inquire_time.append(hour)
        hour += 1
    # Compare to current office hour
    available = []
    for data in status:
        # Cond 1: No schedule office hour
        if 3 not in range(len(data)):
            available.append(data[0])
        # Cond 2: Has schedule, check if conflict
        else:
            no_conflict = True
            for i in inquire_time:
                if i in data[3]:
                    no_conflict = False
                    break
            if no_conflict:
                available.append(data[0])

    # Decide the consultant based on criteria
    compare = []
    for data in status:
        if data[0] in available:
            compare.append(
                data[1] if criteria == 'rate' else data[2]
            )

    if compare:
        index = compare.index(
            max(compare)) if criteria == 'rate' else compare.index(min(compare))

    chosen = available[index] if available else 'No service'

    # Book the office hour
    for data in consultants:
        if data['name'] == chosen:
            # Cond 1: hasn't been booked
            if 'office_hour' not in data:
                data['office_hour'] = inquire_time
            else:
                # Cond 2: has been booked before
                data['office_hour'] += inquire_time

    # return result
    print(chosen)


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
    # your code here
    middle_name = []
    for names in data:
        if len(names) == 2 or len(names) == 3:
            middle_name.append(names[1])
        elif len(names) == 4 or len(names) == 5:
            middle_name.append(names[2])
    
    # Find unique one
    unique_middle = []
    for element in middle_name:
        if middle_name.count(element) == 1:
            unique_middle.append(element)
    # Return the unique middle name
    if unique_middle:
        unique_name = data[middle_name.index(*unique_middle)]
    else:
        unique_name = '沒有'

    # print out result
    print(unique_name)


func("彭大牆", "陳王明雅", "吳明")  # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")  # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")  # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆")  # print 夏曼藍波安


# Task 4
def get_number(index):
    # your code here
    num_sequence = []
    num = 0
    for i in range(0, index, 2):
        num_sequence.extend([num, num + 4, num + 8])
        num += 7
    print(num_sequence[index])


get_number(1)  # print 4
get_number(5)  # print 15
get_number(10)  # print 25
get_number(30)  # print 70

# Task 5
def find(spaces, stat, n):
    # your code here
    check_array = []
    for index, bit in enumerate(stat):
        # check if car can serve
        if bit == 1:
            check_array.append(
                spaces[index] - n if (spaces[index] - n) >= 0 else float('inf'))
        elif bit == 0:
            check_array.append(float('inf'))
    car_index = check_array.index(min(check_array)) if not all(x == float('inf') for x in check_array) else -1
    print(car_index)


find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2)  # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4)  # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4)  # print 2
