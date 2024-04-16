# write/open best solution
import json
with open("03FetchAPI/taipei-attractions-assignment-1.json", mode = "r", encoding= 'utf-8') as file:
    data1 = json.load(file)

with open("03FetchAPI/taipei-attractions-assignment-2.json", mode="r", encoding='utf-8') as file:
    data2 = json.load(file)


## 'stitle' is the Spot title
## 'SERIAL_NO' can be referenced to second json address 
## District from 'address'
## Longitude from 'longitude'
## Latitude form 'latitude'
## ImgURL from 'filelist' but need to slice


# Prepare the csv file to write
import csv
tableSpot = [['SpotTitle', 'District', 'Longitude', 'Latitude', 'ImageURL']]

# extract data from source json
for spot in data1['data']['results']:
    spotTitle = spot['stitle']
    for mrt in data2['data']:
        if mrt['SERIAL_NO'] == spot['SERIAL_NO']:
            district = mrt['address'][5:8]
    longitude = spot['longitude']
    latitude = spot['latitude']
    imgURL = 'https' + spot['filelist'].split("https", 2)[1]
    tableSpot.append([spotTitle,district,longitude,latitude,imgURL])

# write into csv
# 'utf-8' is not working - The \ufeff is a Byte Order Mark that can often be found on Windows UTF-8 files, and it might be confusing csv. Try using utf-8-sig for the encoding.
with open('03FetchAPI/spot.csv', mode='w', encoding='utf-8-sig', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(tableSpot)
