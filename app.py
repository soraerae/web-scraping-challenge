from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.scraped_data

@app.route("/scrape")
def scraper():
    data = mongo.db.scraped_data
    mars_data = scrape_mars.scrape()
    data.update({}, mars_data, upsert=True)
    print(mars_data)
    #return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
