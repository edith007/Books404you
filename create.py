from models import *
from flask import Flask, render_template, request

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://qrpuxrpigcvxar:26bde601461b37b92590a274ba54a0b733036b964e43ec8a3e4698e3c7df8fd3@ec2-174-129-254-218.compute-1.amazonaws.com:5432/dadud12e7137fa"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()


if __name__=='__main__':
    with app.app_context():
        main()