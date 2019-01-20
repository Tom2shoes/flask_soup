from flask import Flask, render_template, redirect
import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mars:scraper1@ds161794.mlab.com:61794/heroku_1gn9n021"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars = mongo.db.scraped_data.find_one()
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scraper():
    mars_data = mongo.db.scraped_data
    data = scrape_mars.scrape()
    mars_data.update({}, data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
