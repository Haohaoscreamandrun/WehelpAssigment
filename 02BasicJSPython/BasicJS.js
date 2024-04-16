// Task 1
function findAndPrint(messages, currentStation) {
  // your code here
  // declare the sequence of Songshan-Xindian Line and Xiaobitan Line
  let greenLine = {
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
    'Xindian': 18,
  };
  let xiaobitanLine = {
    'Qizhang': 0,
    'Xiaobitan': 1,
  };
  // take in the JSON message and process
  let location = new Object();
  for (const [name, sentence] of Object.entries(messages)) {
    // check if sentence include station
    Object.keys({ ...greenLine, ...xiaobitanLine }).forEach((station) => {
      if (sentence.includes(station)) {
        // if yes, add to location pairs
        location[name] = `${station}`;
      }
    });
  }
  // calculate the distance based on currentStation
  var distance = new Object();
  for (const [name, station] of Object.entries(location)) {
    if (Object.keys(greenLine).includes(currentStation)) {
      //if currentStation is on greenLine
      // cond 1: station on greenLine
      // Will be NaN if greenLine['Xiaobitan']
      distance[name] =
        Math.abs(greenLine[station] - greenLine[currentStation]) |
        // cond 2: station not on greenLine, current-Qizhang-station
        (Math.abs(greenLine["Qizhang"] - greenLine[currentStation]) +
          xiaobitanLine[station]);
    } else {
      //if currentStation is not on greenLine
      //cond 1: station on greenLine, current-Qizhang-station
      distance[name] =
        (xiaobitanLine[currentStation] +
          Math.abs(greenLine["Qizhang"] - greenLine[station])) |
        //cond 2: station not on greenLine
        Math.abs(xiaobitanLine[station] - xiaobitanLine[currentStation]);
    }
  }
  // Find the shortest distance and its keys
  let shortestDistance = Math.min(...Object.values(distance));
  let names = [];
  for (const [name, dis] of Object.entries(distance)) {
    if (dis === shortestDistance) {
      names.push(name);
    }
  }
  // print out the result
  console.log(names.join(", "));
}

const messages = {
  Bob: "I'm at Ximen MRT station.",
  Mary: "I have a drink near Jingmei MRT station.",
  Copper: "I just saw a concert at Taipei Arena.",
  Leslie: "I'm at home near Xiaobitan station.",
  Vivian: "I'm at Xindian station waiting for you.",
};

console.time()
findAndPrint(messages, "Wanlong"); // print Mary
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); //print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian
console.timeEnd();
// Can print names locate at different stations with same distance from currentStation.
// Can handle currentStation which's on Xiaobitan Line

// Task 2
// your code here, maybe

function book(consultants, hour, duration, criteria) {
  // your code here
  // sort data
  let status = [];
  for (let i = 0; i < consultants.length; i++) {
    status[i] = Object.values(consultants[i]);
  }
  // confirmation of time slot
  // inquired time
  let inquireTime = [];
  for (let i = 1; i <= duration; i++) {
    inquireTime.push(hour);
    hour++;
  }
  // compare to current office hour
  var available = [];
  status.map((data) => {
    // cond 1: no scheduled office hour
    if (!data[3]) {
      available.push(data[0]);
      // cond 2: has schedule, check if conflict
    } else {
      let noConflict = true;
      for (let i = 0; i < inquireTime.length; i++) {
        // if not, push the name
        if (data[3].includes(inquireTime[i])) {
          noConflict = false;
        }
      }
      noConflict ? available.push(data[0]) : available;
    }
  });
  // decide the consultant base on criteria
  let compare = [];
  status.map((data) => {
    if (available.includes(data[0])) {
      compare.push(criteria === "rate" ? data[1] : data[2]);
    }
  });
  let Index =
    criteria === "rate"
      ? compare.indexOf(Math.max(...compare))
      : compare.indexOf(Math.min(...compare));
  let chosen = available[Index] ? available[Index] : "No Service";
  // Book the office hour
  consultants.map((data) => {
    if (data["name"] === chosen && data["officeHour"] === undefined) {
      data["officeHour"] = inquireTime;
    } else if (data["name"] === chosen && data["officeHour"] !== undefined) {
      data["officeHour"] = data["officeHour"].concat(inquireTime);
    }
  });
  console.log(chosen);
}
const consultants = [
  { name: "John", rate: 4.5, price: 1000 },
  { name: "Bob", rate: 3, price: 1200 },
  { name: "Jenny", rate: 3.8, price: 800 },
];
book(consultants, 15, 1, "price"); // Jenny
book(consultants, 11, 2, "price"); // Jenny
book(consultants, 10, 2, "price"); // John
book(consultants, 20, 2, "rate"); // John
book(consultants, 11, 1, "rate"); // Bob
book(consultants, 11, 2, "rate"); // No Service
book(consultants, 14, 3, "price"); // John

// Modify in place of const consultants

// Task 3
function func(...data) {
  // your code here
  // Take all middlename out in to an array
  let middleName = [];
  data.map((names) => {
    if (names.length === 2 || names.length === 3) {
      middleName.push(names[1]);
    } else if (names.length === 4 || names.length === 5) {
      middleName.push(names[2]);
    }
  });
  // find the unique one
  let uniqueMiddle = middleName.filter((element, index, array) => {
    return array.indexOf(element) === array.lastIndexOf(element);
  });
  // return the unique middlename
  let uniqueName = data[middleName.indexOf(...uniqueMiddle)]
    ? data[middleName.indexOf(...uniqueMiddle)]
    : "沒有";
  console.log(uniqueName);
}
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安

//Task 4
function getNumber(index) {
  // your code here
  let numSequence = [];
  let num = 0;
  for (let i = 0; i < index; i = i + 2) {
    numSequence.push(...[num, num + 4, num + 8]);
    num = num + 7;
  }
  console.log(numSequence[index]);
}
getNumber(1); // print 4
getNumber(5); // print 15
getNumber(10); // print 25
getNumber(30); // print 70

//Task 5 (optional)
function find(spaces, stat, n) {
  // your code here
  let checkArray = [];
  stat.map((bit, index, array) => {
    //check car can serve
    if (bit === 1) {
      checkArray[index] = spaces[index] - n < 0 ? Infinity : spaces[index] - n;
    } else if (bit === 0) {
      checkArray[index] = Infinity;
    }
  });
  let carIndex = checkArray.indexOf(Math.min(...checkArray))
    ? checkArray.indexOf(Math.min(...checkArray))
    : -1;
  console.log(carIndex);
}
find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2); // print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4); // print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4); // print 2
