# Task 1: Parse data from internet and save to files by Python

# fetch from URL
import urllib.request as request
import json
urls = ['https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1',
       'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2']
data = []
for i, url in enumerate(urls):
    with request.urlopen(url) as response:
        data.append(json.load(response))
taipei_attractions = data[0]
station_MRT = data[1]


# write/open best solution
#import json
#with open("03FetchAPI/taipei-attractions-assignment-1", mode = "r", encoding= 'utf-8') as file:
#    taipei_attractions = json.load(file)

#with open("03FetchAPI/taipei-attractions-assignment-2", mode="r", encoding='utf-8') as file:
#    station_MRT = json.load(file)

## Find the desired attributes
# 'stitle' is the Spot title
# 'SERIAL_NO' can be referenced to station_MRT json address
# District from 'address'
# Longitude from 'longitude'
# Latitude form 'latitude'
# ImgURL from 'filelist' but need to slice


# Prepare the list and dictionary to write is csv
import csv
table_spot = []
dict_MRT = {}

# extract data from source json
for spot in taipei_attractions['data']['results']:
    spot_title = spot['stitle']
    for mrt in station_MRT['data']:
        if mrt['SERIAL_NO'] == spot['SERIAL_NO']:
            # get the name of district from address key
            spot_district = mrt['address'][5:8]
            # grouping the spot base on mrt['MRT'] key
            dict_MRT.update({mrt['MRT']: [spot['stitle']]}
                            ) if mrt['MRT'] not in dict_MRT.keys() else dict_MRT[mrt['MRT']].append(spot['stitle'])
                       
    spot_longitude = spot['longitude']
    spot_latitude = spot['latitude']
    # split 2 times and get the second: ['', '://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000848.jpg','://www...']
    spot_imgURL = 'https' + spot['filelist'].split("https", 2)[1]
    # one dict per line in csv
    table_spot.append(
        {'SpotTitle': spot_title,
         'District': spot_district,
         'Longitude': spot_longitude,
         'Latitude': spot_latitude,
         'ImageURL': spot_imgURL})


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
    # access the dict of MRT: [spots]
    for MRT_station, spots in dict_MRT.items():
        # one dict per row in csv, the first column is MRT_station
        row_data = {'MRT_station': MRT_station}

        # give column name for each spot 
        for index, spot in enumerate(spots):
            row_data.update({f'spots_{index+1}': spot})
        # write a single row and loop to next station
        writer.writerow(row_data)

# Task 2:  Parse web page data and save to files by Python (Optional)

def openWeb(url):

    # import library
    import urllib.request as req

    # create request obj with headers info, use this obj to open the site
    request = req.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        'cookie': 'over18=1'
    })

    # extract and open
    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')
        return data

    # print(data)  
    # urllib.error.HTTPError: HTTP Error 403: Forbidden
    # webpage decline connection due to un-human behavior
    # In normal request, there are a lot more information sent to web site: request headers

    # After adding request header we can access but only the 18y confirmation page
    # Cause ppt will put a 'over18' cookie in browser after clicked agree
    # Browser will include this cookie in request headers if it already been given the cookie

def crawlData(url, times):
    current_url = url
    i = 0
    crawl_all = []
    while i < times:
        i += 1
        data = openWeb(current_url)
        # start of crawling
        # pip install BeautifulSoup4
        import bs4,re,csv

        root = bs4.BeautifulSoup(data, features= "html.parser")
        titles = root.find_all(name ='div', class_= 'title')
        
        # get to the url of next page
        # find the a tag that got a string like ‹ 上頁
        next_page_url = "https://www.ptt.cc" + \
        root.find(name='a', string='‹ 上頁')['href']
        # update the current_url
        current_url = next_page_url

        for title in titles:
            if title.a != None: #print if <a> tag exist(not deleted)
                try:
                    # link a parse the article
                    article_url = "https://www.ptt.cc" + (title.a.get('href'))
                    article_data = openWeb(article_url)
                    article_root = bs4.BeautifulSoup(article_data, features="html.parser")
                    push_times_all = article_root.find_all(name='span', class_='push-tag')
                    like_dislike_counts = 0
                    for push_time in push_times_all:
                        
                        if len(re.findall("推|噓", push_time.string)) != 0:
                            like_dislike_counts += 1
                    
                    publish_time = article_root.find_all(
                        name='span', class_='article-meta-value')[3].string
                except IndexError:
                    publish_time = ""
                crawl_all.append({
                    'title': title.a.string,
                    'counts': like_dislike_counts,
                    'publish_time': publish_time
                })
        print(f"Complete the crawling in page {i}")
            
    # write row in the csv file
    with open('03FetchAPI/article.csv', mode='w', encoding='utf-8-sig', newline='') as article_csv_file:
        writer = csv.DictWriter(article_csv_file, fieldnames= ['title', 'counts', 'publish_time'])
        writer.writerows(crawl_all)
        print('Data has been saved to article.csv')
    


crawlData('https://www.ptt.cc/bbs/Lottery/index.html',3)
# crawl for 3 pages
