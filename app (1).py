import csv
from bs4 import BeautifulSoup
import requests
import json

base_url = 'https://teileshop.diederichs.com'
listof_url = '/index.php?action=article&manufacturer=32328&vehicle=698422'
ex : base_url = base_url.encode('utf8')




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

    vehicle_url = f"{base_url}/index.php?action=article&manufacturer={manufacturer}&vehicle={vehicle_id}"
    r = requests.get(vehicle_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, features="html.parser")

    items = soup.find_all('a', attrs={'popup': 'detail'})

    Items = []
    for item in items:
        item_url = item.get('href')
        itemDetails = getItemDetails(base_url + '/' + item_url + '&ajax=true')
        Items.append(itemDetails)
    
    return Items

def main():
    manufacturer = 32328
    vehicle = 698422

    with open('output.csv', 'w+', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(["Item id", "Manufacturer", "Vehicle id", "Description", "Image URL"])

        # for item from list:
        #     manufacture = 
        #     vehicle = ?
        #for itemobj in parse_page(manufacturer, vehicle):
            #row = [itemobj.item_id, manufacturer, vehicle, itemobj.description, itemobj.image_url ]
            #write.writerow(row)
            # print(json.dumps(itemobj.__dict__) + '\n\n')

if __name__=="__main__":
    main()


    with open('output.csv', 'w+') as f:
     write = csv.writer(f)
     write.writerow(["Item id", "Manufacturer", "Vehicle id", "Description", "Image URL"])
     # for row in rows:

#     for itemobj in Items:
#         row = [itemobj.item_id, 32328, 698422, itemobj.description, itemobj.image_url ]
#         write.writerow(row)
        # print(json.dumps(itemobj.__dict__) + '\n\n')
