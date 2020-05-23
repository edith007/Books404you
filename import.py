import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine("postgres://qrpuxrpigcvxar:26bde601461b37b92590a274ba54a0b733036b964e43ec8a3e4698e3c7df8fd3@ec2-174-129-254-218.compute-1.amazonaws.com:5432/dadud12e7137fa")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn , :title, :author, :year)",
                    {'isbn':isbn , 'title':title , 'author':author, 'year':year})
        print(f"Added {isbn}, {title} by {author} in {year}")
    db.commit()

if __name__ == "__main__":
    main()