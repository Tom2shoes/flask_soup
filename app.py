from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_surfing


app = Flask(__name__)






if __name__ == "__main__":
    app.run(debug=True)
