# write/open best solution
import json
with open("03FetchAPI/taipei-attractions-assignment-1.json", mode = "r", encoding= 'utf-8') as file:
    taipei_attractions = json.load(file)

with open("03FetchAPI/taipei-attractions-assignment-2.json", mode="r", encoding='utf-8') as file:
    station_MRT = json.load(file)


## 'stitle' is the Spot title
## 'SERIAL_NO' can be referenced to second json address 
## District from 'address'
## Longitude from 'longitude'
## Latitude form 'latitude'
## ImgURL from 'filelist' but need to slice


# Prepare the csv file to write
import csv
table_spot = []
dict_MRT = {}

# extract data from source json
for spot in taipei_attractions['data']['results']:
    spot_title = spot['stitle']
    for mrt in station_MRT['data']:
        if mrt['SERIAL_NO'] == spot['SERIAL_NO']:
            spot_district = mrt['address'][5:8]
            dict_MRT.update({mrt['MRT']: [spot['stitle']]}
                            ) if mrt['MRT'] not in dict_MRT.keys() else dict_MRT[mrt['MRT']].append(spot['stitle'])
                       
    spot_longitude = spot['longitude']
    spot_latitude = spot['latitude']
    spot_imgURL = 'https' + spot['filelist'].split("https", 2)[1] #split 2 times and get the second
    table_spot.append(
        {'SpotTitle': spot_title,
         'District': spot_district,
         'Longitude': spot_longitude,
         'Latitude': spot_latitude,
         'ImageURL': spot_imgURL})



print(dict_MRT)
# write into csv
# 'utf-8' is not working - The \ufeff is a Byte Order Mark that can often be found on Windows UTF-8 files, and it might be confusing csv. Try using utf-8-sig for the encoding.
with open('03FetchAPI/spot.csv', mode='w', encoding='utf-8-sig', newline='') as spot_csv_file:
    spot_field_names = ['SpotTitle', 'District', 'Longitude', 'Latitude', 'ImageURL']
    writer = csv.DictWriter(spot_csv_file, fieldnames= spot_field_names)
    writer.writeheader()
    writer.writerows(table_spot)

with open('03FetchAPI/mrt.csv', mode='w', encoding='utf-8-sig', newline='') as mrt_csv_file:
    # give field names based on max number of spot
    mrt_field_name = ['MRT_station']+[f'spots_{i+1}' for i in range(
        max(len(value) for value in dict_MRT.values()))]
    writer = csv.DictWriter(mrt_csv_file, fieldnames= mrt_field_name)
    for MRT_station, spots in dict_MRT.items():
        row_data = {'MRT_station': MRT_station}
        # give column name for each spot 
        for index, spot in enumerate(spots):
            row_data.update({f'spots_{index+1}': spot})
        # write a single row and loop to next station
        writer.writerow(row_data)


