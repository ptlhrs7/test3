# Import dependencies
import requests
import json
import pandas as pd
from datetime import *
import sqlalchemy as sql
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy_utils import database_exists, create_database
from flask import Flask, render_template, redirect, url_for, request
from flask import Flask, jsonify
from api_keys import password, yelp_key, g_key
import logging
from getdata import getCoordinates, getYelpPlaces, updateTable, getFromTable



# Create an instance of Flask
app = Flask(__name__)


# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Update display route
@app.route("/Update")
def update():
    print("Redirected to Update route.")
    return ()
    

# Define the categories
categories = ['gyms', 'hotels', 'restaurants', 'entertainment', 'landmarks']


# Get Gym info from database and/or Yelp and send back to client
@app.route("/Gyms", methods=['GET', 'POST'])
def getGyms():
    print("Gyms route accessed.")
    search_area = request.get_json(force=True)
    print(f"Searching for: {search_area['search']}")

    # Step 1: Get coordinates and identifying info for search_area
    latitude, longitude, search_DF = getCoordinates(search_area['search'])

    # Step 2:  See if those coordinates already exist in the database
    search_table = "searches"
    search_item = search_DF.iloc[0, 0]
    result_DF = getFromTable(search_table, search_item, return_json=False)
    
    # Step 3:  If they don't, then get places from Yelp and place into database
    if result_DF.empty:
        updateTable(search_DF, search_table)
        for category in categories:
            table_DF = getYelpPlaces(latitude, longitude, category)
            print(f"Retrieved Yelp data for {category}")
            updateTable(table_DF, category)

    # Step 4:  Retrieve data from database
    output_JSON = getFromTable("gyms", search_item, return_json=True)

    # Step 5:  Send data back to client
    print(json.dumps(output_JSON,indent=4))
    return(output_JSON)

# Get Hotel info from database and/or Yelp and send back to client
@app.route("/Hotels", methods=['GET', 'POST'])
def getHotels():
    print("Hotels route accessed.")
    search_area = request.get_json(force=True)
    print(f"Searching for: {search_area['search']}")

    # Step 1: Get coordinates and identifying info for search_area
    latitude, longitude, search_DF = getCoordinates(search_area['search'])

    # Step 2:  See if those coordinates already exist in the database
    search_table = "searches"
    search_item = search_DF.iloc[0, 0]
    result_DF = getFromTable(search_table, search_item)
    
    # Step 3:  If they don't, then get places from Yelp and place into database
    if result_DF.empty:
        updateTable(search_DF, search_table)
        for category in categories:
            table_DF = getYelpPlaces(latitude, longitude, category)
            print(f"Retrieved Yelp data for {category}")
            updateTable(table_DF, category)

    # Step 4:  Retrieve data from database
    output_JSON = getFromTable("hotels", search_item, return_json=True)

    # Step 5:  Send data back to client
    print(json.dumps(output_JSON,indent=4))
    return(output_JSON)


# Get Restaurant info from database and/or Yelp and send back to client
@app.route("/Restaurants", methods=['GET', 'POST'])
def getRestaurants():
    print("Restaurants route accessed.")
    search_area = request.get_json(force=True)
    print(f"Searching for: {search_area['search']}")

    # Step 1: Get coordinates and identifying info for search_area
    latitude, longitude, search_DF = getCoordinates(search_area['search'])

    # Step 2:  See if those coordinates already exist in the database
    search_table = "searches"
    search_item = search_DF.iloc[0, 0]
    result_DF = getFromTable(search_table, search_item)
    
    # Step 3:  If they don't, then get places from Yelp and place into database
    if result_DF.empty:
        updateTable(search_DF, search_table)
        for category in categories:
            table_DF = getYelpPlaces(latitude, longitude, category)
            print(f"Retrieved Yelp data for {category}")
            updateTable(table_DF, category)

    # Step 4:  Retrieve data from database
    output_JSON = getFromTable("restaurants", search_item, return_json=True)

    # Step 5:  Send data back to client
    print(json.dumps(output_JSON,indent=4))
    return(output_JSON)


# Get Entertainment info from database and/or Yelp and send back to client
@app.route("/Entertainment", methods=['GET', 'POST'])
def getEntertainment():
    print("Entertainment route accessed.")
    search_area = request.get_json(force=True)
    print(f"Searching for: {search_area['search']}")

    # Step 1: Get coordinates and identifying info for search_area
    latitude, longitude, search_DF = getCoordinates(search_area['search'])

    # Step 2:  See if those coordinates already exist in the database
    search_table = "searches"
    search_item = search_DF.iloc[0, 0]
    result_DF = getFromTable(search_table, search_item)
    
    # Step 3:  If they don't, then get places from Yelp and place into database
    if result_DF.empty:
        updateTable(search_DF, search_table)
        for category in categories:
            table_DF = getYelpPlaces(latitude, longitude, category)
            print(f"Retrieved Yelp data for {category}")
            updateTable(table_DF, category)

    # Step 4:  Retrieve data from database
    output_JSON = getFromTable("entertainment", search_item, return_json=True)

    # Step 5:  Send data back to client
    print(json.dumps(output_JSON,indent=4))
    return(output_JSON)


# Get Attractions info from database and/or Yelp and send back to client
@app.route("/Attractions", methods=['GET', 'POST'])
def getAttractions():
    print("Attractions route accessed.")
    search_area = request.get_json(force=True)
    print(f"Searching for: {search_area['search']}")

    # Step 1: Get coordinates and identifying info for search_area
    latitude, longitude, search_DF = getCoordinates(search_area['search'])

    # Step 2:  See if those coordinates already exist in the database
    search_table = "searches"
    search_item = search_DF.iloc[0, 0]
    result_DF = getFromTable(search_table, search_item)
    
    # Step 3:  If they don't, then get places from Yelp and place into database
    if result_DF.empty:
        updateTable(search_DF, search_table)
        for category in categories:
            table_DF = getYelpPlaces(latitude, longitude, category)
            print(f"Retrieved Yelp data for {category}")
            updateTable(table_DF, category)

    # Step 4:  Retrieve data from database
    output_JSON = getFromTable("landmarks", search_item, return_json=True)

    # Step 5:  Send data back to client
    print(json.dumps(output_JSON,indent=4))
    return(output_JSON)



# defining main function
if __name__ == "__main__":
    app.run(debug=True)
    
    
