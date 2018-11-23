import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    file = open("books.csv", "r")
    reader = csv.reader(file)

    # Skip the first line as it only contains column labels but breaks db.execute
    # due to incorrect data types being passed.
    firstLine = True

    for isbn, title, author, year in reader:
        if firstLine:
            firstLine = False
            continue

        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author, "year": year})

    db.commit()


if __name__ == "__main__":
    main()
