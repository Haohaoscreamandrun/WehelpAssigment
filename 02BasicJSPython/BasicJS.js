// Task 1
function findAndPrint(messages, currentStation){
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
    'Xindian': 18
  }
  let xiaobitanLine = {
    'Qizhang': 0,
    'Xiaobitan': 1
  }
  // take in the JSON message and process
  let location = new Object();
  for (const[name, sentence] of Object.entries(messages)){
    // check if sentence include station
    Object.keys({...greenLine,...xiaobitanLine}).forEach((station) =>{
      if(sentence.includes(station)){
        // if yes, add to location pairs
        location[name] = `${station}`
      }
    })
  }
  // calculate the distance based on currentStation
  var distance = new Object();
  for (const[name, station] of Object.entries(location)){
    if(Object.keys(greenLine).includes(currentStation)){
      //if currentStation is on greenLine
      // cond 1: station on greenLine
      // Will be NaN if greenLine['Xiaobitan']
      distance[name] = Math.abs(greenLine[station]-greenLine[currentStation]) | 
      // cond 2: station not on greenLine, current-Qizhang-station 
        (Math.abs(greenLine['Qizhang']-greenLine[currentStation]) + xiaobitanLine[station])
    }else{
      //if currentStation is not on greenLine
        //cond 1: station on greenLine, current-Qizhang-station 
      distance[name] = (xiaobitanLine[currentStation] + Math.abs(greenLine['Qizhang']-greenLine[station])) | 
        //cond 2: station not on greenLine
        Math.abs(xiaobitanLine[station]-xiaobitanLine[currentStation])
    }
  }
  // Find the shortest distance and its keys
  let shortestDistance = Math.min(...Object.values(distance))
  let names = []
 for (const[name, dis] of Object.entries(distance)){
    if (dis === shortestDistance){
      names.push(name)
    }
  }
  // print out the result
  console.log(names.join(', '))
}

const messages = {
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Leslie": "I'm at home near Xiaobitan station.",
    "Vivian": "I'm at Xindian station waiting for you."
  }

findAndPrint(messages,"Wanlong"); // print Mary
findAndPrint(messages,"Songshan"); // print Copper
findAndPrint(messages,"Qizhang"); // print Leslie
findAndPrint(messages,"Ximen"); //print Bob
findAndPrint(messages,"Xindian City Hall"); // print Vivian

// Can print names locate at different stations with same distance from currentStation.
// Can handle currentStation which's on Xiaobitan Line

