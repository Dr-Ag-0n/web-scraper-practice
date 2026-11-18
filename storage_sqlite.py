import sqlite3
import csv

def storage(csv_path, db_path):
    db = sqlite3.connect(db_path)
    try:
        db.execute("""
                   CREATE TABLE IF NOT EXISTS books (
                       title TEXT NOT NULL,
                       href TEXT PRIMARY KEY NOT NULL,
                       price_pence INTEGER,
                       rating INTEGER
                   )
                   """)

        with open(csv_path, "r", encoding="utf-8", newline="") as file:
            loaded_books = list(csv.DictReader(file))

        for loaded_book in loaded_books:
            title = loaded_book["title"]
            href = loaded_book["href"]
            price_pence = int(loaded_book["price_pence"])
            rating = int(loaded_book["rating"])
            db.execute(
                "INSERT INTO books (title, href, price_pence, rating) VALUES (?, ?, ?, ?) ON CONFLICT(href) DO NOTHING",
                (title, href, price_pence, rating)
            )
        db.commit()
        print(db.execute("SELECT COUNT(*) FROM books").fetchone()[0])
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        
def main():
    storage("books.csv", "books.db")
    
if __name__ == "__main__":
    main()