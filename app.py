from bs4 import BeautifulSoup
import requests
import json
import csv
import shutil
import os

base_url = 'https://teileshop.diederichs.com'

with open('lists.txt') as f:
    urls = f.readlines()

with open('output.csv', 'w+', encoding='utf-8') as g:
                write = csv.writer(g)
                write.writerow(["Item id", "Manufacturer", "Vehicle id", "Description", "Image URL"])

path = 'Images'
if not os.path.exists(path):
    os.mkdir(path)
    print("Directory " , path ,  " Created ")
else:    
    print("Directory " , path ,  " already exists")

for url1 in urls:
    inputauto_url = url1.split('https://teileshop.diederichs.com', 1)[1]
    manu = url1.split('=', 2)[2].split('&')[0]
    vehicle_id = url1.split('=')[3].split('&')[0]
    class Item:
        item_id: str
        image_url: str
        description: str

    def getItemDetails(url: str):
        r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(r.content, features="html.parser")

        item = Item()

        item.image_url = base_url + '/' + soup.find('img', id='zoomimage').get('src')
        for td in soup.find_all(style='vertical-align:top'):
            if td.get_text() == 'Item:':
                item.item_id = td.next_sibling.get_text()
            if td.get_text() == 'Description:':
                item.description = td.next_sibling.get_text().replace('\t', '')
        print("Fetched details for item " + item.item_id)
        return item


    vehicle_url = base_url + inputauto_url
    r = requests.get(vehicle_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, features="html.parser")

    items = soup.find_all('a', attrs={'popup': 'detail'})


    Items = []
    for item in items:
        item_url = item.get('href')
        itemDetails = getItemDetails(base_url + '/' + item_url + '&ajax=true')
        Items.append(itemDetails)

    for itemobj in Items:
        print(json.dumps(itemobj.__dict__) + '\n\n')
    
        with open('output.csv', 'a', encoding='utf-8') as f:
                write = csv.writer(f)
                write.writerow([itemobj.item_id, manu, vehicle_id, itemobj.description, itemobj.image_url])
        
        url2 = json.dumps(itemobj.image_url)
        url2 = url2.split("\n")[0].split("\"")[1]
        res = requests.get(url2, stream = True)
        filenameq = os.path.join('.\Images', url1.split('https://teileshop.diederichs.com/temp/image/popup/')[1].split('\"')[0])
        if res.status_code == 200:
            with open(filenameq,'wb') as f:
                shutil.copyfileobj(res.raw, f)
                print('Image sucessfully Downloaded: ',filenameq)