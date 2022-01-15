# pip install sqlalchemy-utils

# This function uses Google Geocode to convert the user's search into latitude / longitude coordinates.

#Imports
import requests
import json
import pandas as pd
from datetime import *
import sqlalchemy as sql
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy_utils import database_exists, create_database
from api_keys import password, yelp_key, g_key
import logging

# Set the logging level (used for debugging)
logging.basicConfig(level=logging.ERROR)

engine = sql.create_engine(f"postgresql://postgres:{password}@localhost/TravelBuddyDB")
session = Session(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
searches = Base.classes.searches



############################
def new_user():
    try:
        engine = sql.create_engine(f"postgresql://postgres:{password}@localhost/TravelBuddyDB")
        print("Connection to PostgreSQL successful.")
        if not database_exists(engine.url):
            create_database(engine.url)
            print("New database created: TravelBuddyDB")
        else:
            print("TravelBuddyDB found.")
    except:
        print("Failed to connect.")
###################

def  db_check(target):
    #test_target = '38118'
    test_days = 0

    # Get Google developer API key from file: api_keys.py
    from api_keys import g_key

    # Test Target (this will be passed in from calling routine)

    # Build the endpoint URL
    target_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={target}&key=APIKey"


    # Run a request to the endpoint and convert result to a json
    response = requests.get(target_url)
    geo_data = response.json()

    # Extract latitude and longitude and create key variable
    lat = round(geo_data["results"][0]["geometry"]["location"]["lat"],2)
    lng = round(geo_data["results"][0]["geometry"]["location"]["lng"],2)
    loc_key = f'{lat},{lng}'
    #lk_check = entry_data['loc_key'][0]

    input_date = date.isoformat(date.today())

    #Check if Data Exists

    check_query = session.query(searches.loc_key, searches.input_date).\
        filter(searches.loc_key == loc_key).first()
    session.close()

    # If data does not exist check_query will be false, if it does exist, we will check for date
    if check_query is None:
        exist_test = False
        print('no data exists')
        build_search_entry(geo_data, lat, lng, loc_key, input_date, exist_test, target)
        
    else:
        exist_test = True
        print(f'data for {loc_key} already exists')

    #checking to determine if date is less than our minimum date for keeping data. 

        (db_key,db_date) = check_query
        check_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        check_date = check_date - timedelta(days = test_days)
        old_data_check = db_date < check_date

        #If data is old, it will be removed from the database using a session query. 

        if old_data_check == True:
            session.query(searches).filter(searches.loc_key == loc_key).delete()
            session.commit()
            print('Data Removed')
            build_search_entry(geo_data, lat, lng, loc_key, input_date, exist_test, target, old_data_check)
        else: 
            print(f'Location {loc_key} is already in Database.')

    ###############################################################
# function to build  search entry. 

def build_search_entry(geo_data, lat, lng, loc_key, input_date, exist_test, target, old_data_check = False):

     #Determine size of output
    g_range = len(geo_data['results'][0]["address_components"])

    #Declare empty variables - in case an entry is missing one. 

    search_data = {}
    area = ''
    city = ''
    state = ''
    country = ''

    #find tags, and assign values. 

    for y in range(g_range):
        if geo_data["results"][0]["address_components"][y]["types"][0] == "neighborhood":
            area = geo_data["results"][0]["address_components"][y]["long_name"]
        if geo_data["results"][0]["address_components"][y]["types"][0] == "locality":
            city = geo_data["results"][0]["address_components"][y]["long_name"]
        if geo_data["results"][0]["address_components"][y]["types"][0] == "administrative_area_level_1":
            state = geo_data["results"][0]["address_components"][y]["long_name"]
        if geo_data["results"][0]["address_components"][y]["types"][0] == "country":
            country = geo_data["results"][0]["address_components"][y]["long_name"]
        if area == '':
            area = 'N/A'

    #Find Current Date

    #create dictionary for search table

    search_data = {'loc_key': loc_key, 'target': target, 'area': area, 'city': city, 'loc_state': state, 'country': country, 'input_date': input_date}

    #assign dictionary to dataframe

    entry_data = pd.DataFrame(search_data, index=[0])

    # Output the coordinates
    print(f"Latitude: {lat}")
    print(f"Longitude: {lng}")
    print(entry_data)

    Yelp_Pull_Enter(exist_test, old_data_check, lat, lng, entry_data, loc_key)

########################################################################
#yelp entry formula

def Yelp_Pull_Enter(exist_test, old_data_check, lat, lng, entry_data, loc_key):
    
    if (exist_test == False) or (exist_test == True and old_data_check == True):

        categories = ['restaurants', 'bars', 'hotels', 'gyms', 'landmarks', 'arts']

        # Test parameters (these will be passed in from calling routine)
        input_lat = lat
        input_lon = lng
        #category = 'restaurants'

        # Construct the search parameters
        headers = {'Authorization': 'Bearer {}'.format(yelp_key)}
        url = 'https://api.yelp.com/v3/businesses/search'

        #Insert Search Table Row

        table_name = 'searches'

        with engine.connect() as cnxn:  # the connection will automatically close after executing the with block
                        entry_data.to_sql(table_name, cnxn, if_exists="append", index=False)
                        print(f"{table_name} successfully inserted.")  

        for category in categories:

            table_name = category

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
                print(f"A Yelp error has occured: {response.status_code} {response.reason}")    
                #return ("N/A")

            num_places = len(yelp_data["businesses"])

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
                price_available =  "price" in place
                search_zip.append(f'{input_lat},{input_lon}')
                bus_id.append(place['id'])
                name.append(place['name'])
                if price_available:
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

            # Convert dictionary to dataframe
            yelp_DF = pd.DataFrame(yelp_dict)

            try:
                with engine.connect() as cnxn:  # the connection will automatically close after executing the with block
                            yelp_DF.to_sql(table_name, cnxn, if_exists="append", index=False)
                            print(f"{table_name} successfully inserted.")  
            except: 
                print('There was an error connecting with the database.')
            # Return the dataframe
            #print(yelp_DF.head())

    else:
        print(f'Location {loc_key} is already in Database.')


def getFromTable(table_name, search_item, num_rows=5, sort_by="rating", lowest_to_highest=False, return_json=False):
    # This function searches the PostgreSQL database "TraelBuddyDB" and returns the requested data from the specified table.
    # Make sure your password is saved in file "api_keys.py".
    # Input parameters: 
    #   table_name: string (required) (the name of the table to search in the SQL database)
    #   search_item: string or numeric (required) (the record identifier to search for in table_name in column "loc_key")
    #   num_rows: integer (optional, defaults to 5) (the number of rows to return)
    #   sort_by: string (optional, defaults to "rating") (the column to sort on)
    #   lowest_to_highest: boolean (optional, defaults to False) (the sorting direction)
    #   return_type: boolean (optional, defaults to False) (selects wheter a JSON is returned or a dataframe) 
    # Function returns: 
    #   either a JSON or a dataframe containing the rows of data found in table_name whose "loc_key" macthes search_item
    #   or an empty dataframe if nothing is found or if table_name or TravelBuddyDB don't exist

    # Define the search column
    search_column = "loc_key"
    
    # Connect to database TravelBuddyDB
    engine = sql.create_engine(f"postgresql://postgres:{postgresql_pwd}@localhost/TravelBuddyDB")
    logging.info("Connection to PostgreSQL successful.")

    # Check if the database exists and get a list of the tables it contains
    if database_exists(engine.url):
        table_list = sql.inspect(engine).get_table_names()
        logging.info(table_list)

        # Check if table_name is one of the tables in the database
        if table_name in table_list:
            with engine.connect() as cnxn:

                # Check if search_item is present in the table
                result = engine.execute(f'Select * from "{table_name}" where "{search_column}" = \'{search_item}\'').fetchall()
                if len(result) > 0:

                    # If so, create a dataframe from the table with only the rows containing search_item
                    result_DF = pd.read_sql(f'Select * from "{table_name}" where "{search_column}" = \'{search_item}\'', cnxn)
                else:

                    # If not, create an empty dataframe
                    result_DF = pd.DataFrame()

        # If table_name does not exist in the database, create an empty dataframe
        else:
            logging.info(f"{table_name} does not exist.")
            result_DF = pd.DataFrame()  # table_name does not exist in the database

    # If TravelBuddyDB does not exist, create an empty dataframe
    else:
        logging.info("TravelBuddyDB does not exist.")
        result_DF = pd.DataFrame()  # TravelBuddyDB has not been created yet
        
    # Sort and truncate the dataframe as specified by the input parameters
    if not result_DF.empty and table_name != "searches":
        result_DF = result_DF.sort_values([sort_by], ascending=lowest_to_highest).head(num_rows)
    
    # Exit and return a JSON or a dataframe, depending on the return_json parameter 
    if return_json:
        return(json.loads(result_DF.to_json(orient="records")))
    else:
        return(result_DF)

    
############################################################################################################################

# Test of function getFromTable
# categories = ['restaurants', 'bars', 'hotels', 'gyms', 'landmarks', 'arts']
# table_name = categories[1]
# loc_key = "33.84,-84.41"
# new_DF = getFromTable(table_name, loc_key)
# new_DF


#db_check('Buckhead')

new_user()