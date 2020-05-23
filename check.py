from sqlalchemy import create_engine
from flask import jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import sha384

engine = create_engine("postgresql://postgres:3gk9yy=l@localhost:5432/users")
db = scoped_session(sessionmaker(bind=engine))


def main():
    book_id = input("Enter book id :")
    book = db.execute("SELECT * FROM books WHERE book_id=:book_id",
                            {'book_id':book_id}).fetchall()
    if len(book)==0:
        print("No book found")
        return ("No Book found")
    print(book)
if __name__=="__main__":
    main()