from bs4 import BeautifulSoup
from scraper import get_booklist

def test_parse_one_book():
    with open("tests/fixtures/one_book.html", "r", encoding="utf-8") as file:
        html_raw = file.read()
        soup = BeautifulSoup(html_raw, "html.parser")
        booklist = get_booklist(soup, "https://books.toscrape.com/")
        
        assert len(booklist) == 1
        book = booklist[0]
        assert book["title"] == "A Light in the Attic"
        assert book["href"] == "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        assert book["price_pence"] == 5177 
        assert book["rating"] == 3
        
def test_rating_class_order():
    with open("tests/fixtures/one_book.html", "r", encoding="utf-8") as file:
        html_raw = file.read()
        soup = BeautifulSoup(html_raw, "html.parser")
        booklist = get_booklist(soup, "https://books.toscrape.com/")
        
        book = booklist[0]
        assert book["rating"] == 3