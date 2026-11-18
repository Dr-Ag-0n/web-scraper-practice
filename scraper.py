import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv

allowed_ratings = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def get_booklist(soup, cur_url):
    book_elements = soup.select("li.col-xs-6.col-sm-4.col-md-3.col-lg-3")

    booklist = []

    for book_element in book_elements:
        title_element = book_element.select_one("h3 > a")
        price_element = book_element.select_one("p.price_color")
        rating_element = book_element.select_one("p.star-rating")

        if title_element is None:
            print("Title missing")
            continue
        if price_element is None:
            print("Price missing")
            continue
        if rating_element is None:
            print("Rating missing")
            continue

        title_raw = title_element.get("title")
        if title_raw is None:
            print("Title raw missing")
            continue
        title = title_raw.strip()
        if title == "":
            print("Title raw missing")
            continue
            
        href_raw = title_element.get("href")
        if href_raw is None:
            print("Href raw missing")
            continue
        href = href_raw.strip()
        if href == "":
            print("Href raw missing")
            continue
        detail_url = urljoin(cur_url, href)

        price_raw = price_element.text
        price = price_raw.strip()
        if price == "":
            print("Price raw missing")
            continue
        if not price.startswith("£"):
            print("Invalid price")
            continue
        whole_price = price[1:]
        pounds, pence = whole_price.split(".")
        price_in_pence = int(pounds) * 100 + int(pence)

        rating_classes = rating_element.get("class", [])
        rating =  None
        for rating_class in rating_classes:
            if rating_class in allowed_ratings:
                rating = allowed_ratings[rating_class]
                break
        if rating is None:
            print("Rating missing")
            continue
        
        book = {
            "title": title,
            "href": detail_url,
            "price_pence": price_in_pence,
            "rating": rating
        }
        
        booklist.append(book)
    
    return booklist
    
def find_next_page_url(soup, cur_url):
    next_element = soup.select_one("li.next > a")
    if next_element is None:
        return None
    else:
        next_href_raw = next_element.get("href")
        if next_href_raw is None:
            return None
        else:
            next_href = next_href_raw.strip()
            if next_href == "":
                return None
            else:
                next_detail_href = urljoin(cur_url, next_href)
                return next_detail_href

def save(books, csv_path):
    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "href", "price_pence", "rating"])
        writer.writeheader()
        writer.writerows(books)

def main():
    URL = "https://books.toscrape.com/"
    visiting_url = URL
    booklist = []
    for _ in range(3):
        page = requests.get(visiting_url, timeout=10)

        page.raise_for_status()

        soup = BeautifulSoup(page.content, "html.parser")
        booklist.extend(get_booklist(soup, page.url))
        next_url = find_next_page_url(soup, page.url)
        if next_url is not None:
            visiting_url = next_url
        else:
            break
        time.sleep(0.5)
        
    save(booklist, "books.csv")

if __name__ == "__main__":
    main()