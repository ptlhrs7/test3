# This program is for testing the functions in "travel_buddy2.6.py"

# Imports
import pandas as pd
import requests
import json
from datetime import *
import sqlalchemy as sql
from sqlalchemy_utils import database_exists, create_database

# Import the API and database handling functions
from travel_buddy_26 import getCoordinates, getYelpPlaces, updateTable, getFromTable

# Get API keys and SQL password from file: api_keys.py
from api_keys import g_key
from api_keys import yelp_key
from api_keys import postgresql_pwd

#########################################################################################################################################

# Step 1:  Get search from user

categories = ['restaurants', 'bars', 'hotels', 'gyms', 'landmarks', 'arts']
search_type = categories[2]

search_area = "30126"  # Enter test search here (this will eventually be supplied by Flask)

# Step 2:  Call Google API and get coordinate info

latitude, longitude, search_DF = getCoordinates(search_area)

if latitude == "N/A":
    print("Please enter a neighborhood, city, address, or zip code, or any combination.")
else:

    # Step 3:  See if those coordinates already exist in the database

    search_table = "searches"
    search_item = search_DF.iloc[0, 0]

    result_DF = getFromTable(search_table, search_item)
    if result_DF.empty:

        # Step 4:  If they don't, then get places from Yelp and place into database

        updateTable(search_DF, search_table)
        for category in categories:
            table_DF = getYelpPlaces(latitude, longitude, category)
            print(f"Retrieved Yelp data for {category}")
            updateTable(table_DF, category)

    # Step 5:  Retrieve data from database

    output_DF = getFromTable(search_type, search_item)

    # Step 6:  Send data back to user

    print(f"\n {search_type} found in {search_area}:\n")
    print(output_DF)