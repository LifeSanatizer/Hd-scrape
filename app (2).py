import csv
from bs4 import BeautifulSoup
import requests
import json

base_url = 'https://teileshop.diederichs.com'
new_url ='/index.php?action=article&manufacturer=32328&vehicle=698419'

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

def parse_page(manufacturer, vehicle_id):
    
    vehicle_url =base_url+new_url
    r = requests.get(vehicle_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, features="html.parser")

    items = soup.find_all('a', attrs={'popup': 'detail'})

    Items = []
    for item in items:
        item_url = item.get('href')
        itemDetails = getItemDetails(base_url + '/' + item_url + '&ajax=true')
        Items.append(itemDetails)
    
    return Items
        
for itemobj in item:
  print(json.dumps(itemobj.__dict__) + '\n\n')


# with open('output.csv', 'w+') as f:
#     write = csv.writer(f)
#     write.writerow(["Item id", "Manufacturer", "Vehicle id", "Description", "Image URL"])
#     # for row in rows:

#     for itemobj in Items:
#         row = [itemobj.item_id, 32328, 698422, itemobj.description, itemobj.image_url ]
#         write.writerow(row)
        # print(json.dumps(itemobj.__dict__) + '\n\n')
