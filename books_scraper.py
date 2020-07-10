import requests
from lxml import html
from urllib.parse import urljoin
import csv

books = []

def write_to_csv(data):
    headers = ['title', 'price' , 'avialability',]
    with open('books.csv', 'w', encoding='utf-8') as f:
        writer= csv.DictWriter(f,headers)
        writer.writeheader()
        writer.writerows(data)





def scraping(url):
    resp = requests.get(url=url , headers={
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61'
    })

    tree = html.fromstring(html=resp.content)
    books_main = tree.xpath("//div/ol[@class='row']/li")

    for book in books_main:
        b = {
            'title': book.xpath(".//article[@class='product_pod']/h3/a/@title")[0].strip(),
            'price': book.xpath(".//div[@class='product_price']/p[1]/text()")[0].strip(),
            'avialability': book.xpath(".//div[@class='product_price']/p[2]/text()[2]")[0].strip(),
            
        }

        books.append(b)
    next_page = tree.xpath("//ul[@class='pager']/li/a[contains(text(),'next')]/@href")
    if len(next_page) != 0:
        next_page_url = urljoin(base=url, url=next_page[0])
        scraping(url=next_page_url)

scraping(url='http://books.toscrape.com/')

print(len(books))

write_to_csv(books)