#Imports
import pandas as pd
import requests
import json
import logging
from datetime import *
import sqlalchemy as sql
from sqlalchemy_utils import database_exists, create_database

# Get API keys and SQL password from file: api_keys.py
from api_keys import g_key
from api_keys import yelp_key
from api_keys import postgresql_pwd

# Set the logging level (used for debugging)
logging.basicConfig(level=logging.ERROR)

############################################################################################################################

def getCoordinates(search):
    # This function uses Google Geocode to convert the user's search into latitude / longitude coordinates.
    # It returns the latitude, longitude, and a single row dataframe of metadata about the search area.
    # If nothing is found "N/A", "N/A", and an empty dataframe are returned.

    # Build the endpoint URL
    target_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={search}&key={g_key}"

    try:
        # Run a request to the endpoint and convert result to a json
        response = requests.get(target_url)
        geo_data = response.json()
        if len(geo_data["results"]) == 0:
            logging.info("Zero results returned for this search.")
            return("N/A", "N/A", "N/A")
    except:
        # Print an error message if API request failed
        logging.info(f"A Google error has occured: {response.status_code} {response.reason}")
        return("N/A", "N/A", pd.DataFrame())

    # Extract latitude and longitude from the response and create the primary key
    lat = round(geo_data["results"][0]["geometry"]["location"]["lat"], 2)
    lng = round(geo_data["results"][0]["geometry"]["location"]["lng"], 2)
    loc_key = f"{lat},{lng}"

    # Initialize address components (in case any are missing) 
    area = "N/A"
    city = "N/A"
    state = "N/A"
    country = "N/A"

    # Extract address tags from the response
    for address_component in geo_data["results"][0]["address_components"]:
        if address_component["types"][0] == "neighborhood":
            area = address_component["long_name"]
        if address_component["types"][0] == "locality":
            city = address_component["long_name"]
        if address_component["types"][0] == "administrative_area_level_1":
            state = address_component["long_name"]
        if address_component["types"][0] == "country":
            country = address_component["long_name"]

    # Get the Current Date
    input_date = date.isoformat(date.today())

    # Create dictionary for search table
    search_dict = {
        'loc_key': loc_key, 
        'area': area, 
        'city': city, 
        'loc_state': state, 
        'country': country, 
        'input_date': input_date
    }

    # Convert dictionary to dataframe and return
    entry_DF = pd.DataFrame(search_dict, index=[0])
    return(lat, lng, entry_DF)
 
############################################################################################################################

# test of function getCoordinates
# test_search = "Buckhead, GA"
# latitude, longitude, search_DF = getCoordinates(test_search)
# print(f"Latitude: {latitude}")
# print(f"Longitude: {longitude}")
# search_DF

############################################################################################################################

def getYelpPlaces(input_lat, input_lon, category):
    # This function collects data from Yelp API about the category at the passed in coordinates and returns it as a dataframe.

    # Construct the search parameters
    headers = {'Authorization': 'Bearer {}'.format(yelp_key)}
    url = 'https://api.yelp.com/v3/businesses/search'
    params = {
        'categories': category, 
        'latitude': input_lat,
        'longitude': input_lon,
        'limit': 50
    }

    # Run a request to the endpoint and convert to a json
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        yelp_data = response.json()
    except:
        logging.info(f"A Yelp error has occured: {response.status_code} {response.reason}")    
        return(pd.DataFrame())

    # Define empty lists to place data into
    search_zip = []
    bus_id = []
    name = []
    price = []
    rating = []
    address = []
    city = []
    zip_code = []
    phone = []
    img = []
    latitude = []
    longitude = []

    # Populate the lists
    for place in yelp_data["businesses"]:
        search_zip.append(f'{input_lat},{input_lon}')
        bus_id.append(place['id'])
        name.append(place['name'])
        if "price" in place:
            price.append(place['price'])
        else:
            price.append('N/A')  # in case the price rating is missing
        rating.append(place['rating'])
        address.append(place['location']['address1'])
        city.append(place['location']['city'])
        zip_code.append(place['location']['zip_code'])
        latitude.append(place['coordinates']['latitude'])
        longitude.append(place['coordinates']['longitude'])
        phone.append(place['phone'])
        img.append(place['image_url'])

    # Put lists into dictionary
    yelp_dict = {
        'loc_key': search_zip,
        'bus_id': bus_id,
        'bus_name':name,
        'price':price,
        'rating':rating,
        'address':address,
        'city':city,
        'zip_code':zip_code,
        'phone':phone,
        'image':img,
        'latitude':latitude,
        'longitude':longitude 
    }

    # Convert distionary to dataframe and return
    yelp_DF = pd.DataFrame(yelp_dict)
    return(yelp_DF)

############################################################################################################################

# Test of function getYelpPlaces (parameters latitude and longitude were set in previous cell)
# categories = ['restaurants', 'bars', 'hotels', 'gyms', 'landmarks', 'arts']
# table_names = categories
# test_DF = getYelpPlaces(latitude, longitude, categories[1])
# test_DF

############################################################################################################################

def updateTable(DF, table_name):
    # This function inserts a dataframe into a table in the PostgreSQL database.
    # If the dataframe's primary key already exists in the table, those rows are deleted before the
    # new rows are appended onto the end of the table.
    # Make sure your password is saved in file "api_keys.py".

    # Extract Primary Key from dataframe
    loc_key = DF.iloc[0, 0]
    
    # Put dataframes into PostgreSQL database
    try:
        engine = sql.create_engine(f"postgresql://postgres:{postgresql_pwd}@localhost/TravelBuddyDB")
        logging.info("Connection to PostgreSQL successful.")
        if not database_exists(engine.url):
            create_database(engine.url)
            logging.info("New database created: TravelBuddyDB")
        else:
            logging.info("Connection to database TravelBuddyDB successful.")
        try:
            with engine.connect() as cnxn:  # the connection will automatically close after executing the with block
                logging.info("engine.connect")
                tables = sql.inspect(engine).get_table_names()
                if table_name in tables:
                    engine.execute(f'delete from "{table_name}" where "loc_key" = \'{loc_key}\'') # delete rows if loc_key already present
                logging.info("Deleted old table rows.")
                DF.to_sql(table_name, cnxn, if_exists="append", index=False)
                logging.info(f"{table_name} successfully inserted.")            
        except:
            logging.info(f"Failed to create {table_name} table.")
    except:
        logging.info("Failed to connect.")


############################################################################################################################

# Test of function updateTable
# categories = ['restaurants', 'bars', 'hotels', 'gyms', 'landmarks', 'arts']
# table_names = categories
# updateTable(test_DF, categories[1])

############################################################################################################################

def getFromTable(search_table, search_item):
    # This function searches the PostgreSQL database and returns the requested data from the specified table as a dataframe.
    # If the search_item is not present in the table, an empty dataframe is returned.
    # Make sure your password is saved in file "api_keys.py".

    search_column = "loc_key"
    
    engine = sql.create_engine(f"postgresql://postgres:{postgresql_pwd}@localhost/TravelBuddyDB")
    logging.info("Connection to PostgreSQL successful.")
    if database_exists(engine.url):
        tables = sql.inspect(engine).get_table_names()
        logging.info(tables)
        if search_table in tables:
            with engine.connect() as cnxn:
                result = engine.execute(f'Select * from "{search_table}" where "{search_column}" = \'{search_item}\'').fetchall()
                if len(result) > 0:
                    result_DF = pd.read_sql(f'Select * from "{search_table}" where "{search_column}" = \'{search_item}\'', cnxn)
                else:
                    result_DF = pd.DataFrame()
        else:
            logging.info(f"{search_table} does not exist.")
            result_DF = pd.DataFrame()
    else:
        logging.info("TravelBuddyDB does not exist.")
        result_DF = pd.DataFrame()
        
    return(result_DF)

############################################################################################################################

# Test of function getFromTable
# categories = ['restaurants', 'bars', 'hotels', 'gyms', 'landmarks', 'arts']
# table_name = categories[1]
# loc_key = "33.84,-84.41"
# new_DF = getFromTable(table_name, loc_key)
# new_DF

############################################################################################################################

