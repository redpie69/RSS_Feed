from bs4 import BeautifulSoup
import requests
import rfeed
from datetime import *

url='https://kamuilan.sbb.gov.tr'

months = {
    'ocak' : 1,
    'şubat' : 2,
    'mart':3,
    'nisan':4,
    'mayıs':5,
    'haziran':6,
    'temmuz':7,
    'ağustos':8,
    'eylül':9,
    'ekim':10,
    'kasım':11,
    'aralık':12
}

page = requests.get(url,verify=False)
soup = BeautifulSoup(page.content, "html.parser")
adListTag = soup.find('ul',{'id':"nav2"})  
adListDates = adListTag.find_all('li',recursive=False)

feedItems = []

for adListDate in adListDates:
    day = int(adListDate.time.contents[0].string)
    monthStr = str(adListDate.time.contents[1].string).lower().strip()
    month = months[monthStr];
    publishedOn = datetime(datetime.now().year,month=month,day=day)
    links = adListDate.find_all('a')

    for link in links:
        itemUrl = url + "/" +link['href']
        itemTitle = link.find('p',attrs={'class':'alt_p1'}).string
        itemDescription = ''
        for string in link.find('p',attrs={'class':'alt_p1'}).strings:
            itemDescription =' ' + string
        
        item = rfeed.Item(
            title=itemUrl,
            link=itemUrl,
            description=itemDescription,
            guid=rfeed.Guid(itemUrl),
            pubDate=publishedOn
        )
        feedItems.append(item)


feed = rfeed.Feed(
    title='Kamu Personeli Alım İlanları',
    link='https://kamuilan.sbb.gov.tr',
    description='Strateji ve Bütçe Başkanlığı sitesi tek adreste tüm kamu ilanları listesi',
    language='tr',
    items=feedItems
)

print(feed.rss())
