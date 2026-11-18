import csv

with open("books.csv", "r", encoding="utf-8", newline="") as file:
    loaded_books = list(csv.DictReader(file))
    
print(len(loaded_books))