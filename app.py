from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import numpy as np
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time
# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_db
collection = db.mars

#--------------------------------------------------------
# Flask Setup
#--------------------------------------------------------
app = Flask(__name__)

 
#--------------------------------------------------------
# Flask Routes
#-------------------------------------------------------
@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    mars_mission_data = db.mars.find_one()
    
    print(mars_mission_data)

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars=mars_mission_data)
        
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_scrape_data = scrape_mars.scrape()
    
    # Update the Mongo database using update and upsert=True
    db.mars.update({}, mars_scrape_data, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)

#--------------------------------------------------------
# Debug to run app for testing
#--------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)