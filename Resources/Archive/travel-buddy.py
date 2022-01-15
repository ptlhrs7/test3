#Import
import requests
import json
import pandas as pd
from datetime import *

# Get Google developer API key from file: api_keys.py
from api_keys import g_key

# Collect Latitude/Longitude data from google. 

# Target
target = '30350'  # as a test example (it can be anything)
# Build the endpoint URL
target_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={target}&key={g_key}"
# Run a request to endpoint and convert result to json
geo_data = requests.get(target_url).json()

#check to see if target is zip code

#zip_check = target.isnumeric()
#print(json.dumps(geo_data, indent=4, sort_keys=True))

# Extract latitude and longitude

lat = round(geo_data["results"][0]["geometry"]["location"]["lat"],2)
lng = round(geo_data["results"][0]["geometry"]["location"]["lng"],2)
loc_key = f'{lat},{lng}'
#Extract State and Country data.

g_range = len(geo_data['results'][0]["address_components"])

search_data = {}
area = ''
city = ''
state = ''
country = ''

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

input_date = date.isoformat(date.today())
#+ timedelta(days =7)
#input_date_str = input_date.strftime("%d/%m/%Y %H:%M:%S")

search_data = {'Loc_Key': loc_key, 'Area': area, 'City': city, 'State': state, 'Country': country, 'Input Date': input_date}

entry_data = pd.DataFrame(search_data, index=[0])
print(entry_data)


#print(len(geo_data['results'][0]["address_components"]))
#print(type(target))
zip_check = target.isnumeric()
print(zip_check)
# Output the coordinates
print(f"Latitude: {lat}")
print(f"Longitude: {lng}")
print(f'{area},{city},{state},{country}')

#print(geo_data)
#print(json.dumps(geo_data, indent=4, sort_keys=True))
#print(state)

#--------------------------------------

#Collect data from Yelp API

# Import API key
from api_keys import yelp_key

input_lat = lat
input_lon = lng

headers = {'Authorization': 'Bearer {}'.format(yelp_key)}
url = 'https://api.yelp.com/v3/businesses/search'
params = {'categories': 'restaurants', 
          'latitude': input_lat,
          'longitude': input_lon,
          'limit': 50
          }

response = requests.get(url, headers=headers, params=params, timeout=20)

rest_dict = response.json()


#print (number_restaurants)
#print(rest_dict)
#print(json.dumps(rest_dict, indent=4, sort_keys=True))

number_restaurants = len(rest_dict["businesses"])
y=0
search_zip = []
bus_id = []
name = []
price = []
rating = []
address = []
display_address = []
city = []
zip_code = []
phone = []
img = []
latitude = []
longitude = []

for y in range(number_restaurants):
    price_in_dict =  "price" in rest_dict['businesses'][y]

    #print(f'{price_in_dict} {y}')
    #print(rest_dict['businesses'][y])
    search_zip.append(f'{input_lat},{input_lon}')
    name.append(rest_dict['businesses'][y]['name'])
    if price_in_dict == False:
        price.append('N/A')
    else:
        price.append(rest_dict['businesses'][y]['price'])
    rating.append(rest_dict['businesses'][y]['rating'])
    address.append(rest_dict['businesses'][y]['location']['address1'])
    city.append(rest_dict['businesses'][y]['location']['city'])
    zip_code.append(rest_dict['businesses'][y]['location']['zip_code'])
    latitude.append(rest_dict['businesses'][y]['coordinates']['latitude'])
    longitude.append(rest_dict['businesses'][y]['coordinates']['longitude'])
    #display_address.append(rest_dict['businesses'][y]['location']['display_address'])
    phone.append(rest_dict['businesses'][y]['phone'])
    img.append(rest_dict['businesses'][y]['image_url'])

#print(name)
#print(address)
#print(display_address)

#Create dictionary for dataframe
yelp_rest_dict = {
'Search Area': search_zip,
'Name':name,
'Price':price,
'Rating':rating,
'Address':address,
'City':city,
'Zip Code':zip_code,
'Phone':phone,
'Image':img,
'Latitude':latitude,
'Longitude':longitude 
}

#print(yelp_rest_dict['Name'][0])

yelp_data = pd.DataFrame(yelp_rest_dict)

#print(yelp_data)

#-----------------------------------------------

#Bars

bar_params = {'categories': 'bars',
          'latitude': input_lat,
          'longitude': input_lon,
          'limit': 50
          }

bar_response = requests.get(url, headers=headers, params=bar_params, timeout=20)

bar_dict = bar_response.json()

#print(bar_dict)

number_bars = len(bar_dict["businesses"])
y=0
bar_search_zip = []
bar_name = []
bar_price = []
bar_rating = []
bar_address = []
bar_display_address = []
bar_city = []
bar_zip_code = []
bar_phone = []
bar_img = []
bar_latitude = []
bar_longitude = []

for y in range(number_bars):
    price_in_dict =  "price" in bar_dict['businesses'][y]
    bar_search_zip.append(f'{input_lat},{input_lon}')
    bar_name.append(bar_dict['businesses'][y]['name'])
    if price_in_dict == False:
        bar_price.append('N/A')
    else:
        bar_price.append(bar_dict['businesses'][y]['price'])
    bar_rating.append(bar_dict['businesses'][y]['rating'])
    bar_address.append(bar_dict['businesses'][y]['location']['address1'])
    bar_city.append(bar_dict['businesses'][y]['location']['city'])
    bar_zip_code.append(bar_dict['businesses'][y]['location']['zip_code'])
    bar_latitude.append(bar_dict['businesses'][y]['coordinates']['latitude'])
    bar_longitude.append(bar_dict['businesses'][y]['coordinates']['longitude'])
    #display_address.append(rest_dict['businesses'][y]['location']['display_address'])
    bar_phone.append(bar_dict['businesses'][y]['phone'])
    bar_img.append(bar_dict['businesses'][y]['image_url'])

#print(bar_dict)

#Create dictionary for dataframe
yelp_bar_dict = {
'Search Area': bar_search_zip,
'Name':bar_name,
'Price':bar_price,
'Rating':bar_rating,
'Address':bar_address,
'City':bar_city,
'Zip Code':bar_zip_code,
'Phone':bar_phone,
'Image':bar_img,
'Latitude':bar_latitude,
'Longitude':bar_longitude 
}


yelp_bar_data = pd.DataFrame(yelp_bar_dict)

#print(yelp_bar_data)

#-----------------------------------------------

#Gyms 

gym_params = {'categories': 'gyms',
          'latitude': input_lat,
          'longitude': input_lon,
          'limit': 10
          }

gym_response = requests.get(url, headers=headers, params=gym_params, timeout=20)

gym_dict = gym_response.json()

number_gyms = len(gym_dict["businesses"])
y=0
gym_search_zip = []
gym_name = []
gym_rating = []
gym_address = []
gym_display_address = []
gym_city = []
gym_zip_code = []
gym_phone = []
gym_img = []
gym_latitude = []
gym_longitude = []

for y in range(number_gyms):
    gym_search_zip.append(f'{input_lat},{input_lon}')
    gym_name.append(gym_dict['businesses'][y]['name'])
    gym_rating.append(gym_dict['businesses'][y]['rating'])
    gym_address.append(gym_dict['businesses'][y]['location']['address1'])
    gym_city.append(gym_dict['businesses'][y]['location']['city'])
    gym_zip_code.append(gym_dict['businesses'][y]['location']['zip_code'])
    gym_latitude.append(gym_dict['businesses'][y]['coordinates']['latitude'])
    gym_longitude.append(gym_dict['businesses'][y]['coordinates']['longitude'])
    #display_address.append(rest_dict['businesses'][y]['location']['display_address'])
    gym_phone.append(gym_dict['businesses'][y]['phone'])
    gym_img.append(gym_dict['businesses'][y]['image_url'])

#print(gym_dict)

#Create dictionary for dataframe
yelp_gym_dict = {
'Search Area': gym_search_zip,
'Name':gym_name,
'Rating':gym_rating,
'Address':gym_address,
'City':gym_city,
'Zip Code':gym_zip_code,
'Phone':gym_phone,
'Image':gym_img,
'Latitude':gym_latitude,
'Longitude':gym_longitude 
}


yelp_gym_data = pd.DataFrame(yelp_gym_dict)

#print(yelp_gym_data)

#------------------------------------------------

#Hotels

hotel_params = {'categories': 'hotels',
          'latitude': input_lat,
          'longitude': input_lon,
          'limit': 50
          }

hotel_response = requests.get(url, headers=headers, params=hotel_params, timeout=20)

hotel_dict = hotel_response.json()

#print(hotel_dict)

number_hotels = len(hotel_dict["businesses"])
y=0
hotel_search_zip = []
hotel_name = []
hotel_price = []
hotel_rating = []
hotel_address = []
hotel_display_address = []
hotel_city = []
hotel_zip_code = []
hotel_phone = []
hotel_img = []
hotel_latitude = []
hotel_longitude = []

for y in range(number_hotels):
    price_in_dict =  "price" in hotel_dict['businesses'][y]
    hotel_search_zip.append(f'{input_lat},{input_lon}')
    hotel_name.append(hotel_dict['businesses'][y]['name'])
    if price_in_dict == False:
        hotel_price.append('N/A')
    else:
        hotel_price.append(hotel_dict['businesses'][y]['price'])
    hotel_rating.append(hotel_dict['businesses'][y]['rating'])
    hotel_address.append(hotel_dict['businesses'][y]['location']['address1'])
    hotel_city.append(hotel_dict['businesses'][y]['location']['city'])
    hotel_zip_code.append(hotel_dict['businesses'][y]['location']['zip_code'])
    hotel_latitude.append(hotel_dict['businesses'][y]['coordinates']['latitude'])
    hotel_longitude.append(hotel_dict['businesses'][y]['coordinates']['longitude'])
    #display_address.append(rest_dict['businesses'][y]['location']['display_address'])
    hotel_phone.append(hotel_dict['businesses'][y]['phone'])
    hotel_img.append(hotel_dict['businesses'][y]['image_url'])

#print(hotel_dict)

#Create dictionary for dataframe
yelp_hotel_dict = {
'Search Area': hotel_search_zip,
'Name':hotel_name,
'Price':hotel_price,
'Rating':hotel_rating,
'Address':hotel_address,
'City':hotel_city,
'Zip Code':hotel_zip_code,
'Phone':hotel_phone,
'Image':hotel_img,
'Latitude':hotel_latitude,
'Longitude':hotel_longitude 
}


yelp_hotel_data = pd.DataFrame(yelp_hotel_dict)

#print(yelp_hotel_data)

#------------------------------------

#Landmarks

#landmarks 

landmark_params = {'categories': 'landmarks',
          'latitude': input_lat,
          'longitude': input_lon,
          'limit': 25
          }

landmark_response = requests.get(url, headers=headers, params=landmark_params, timeout=20)

landmark_dict = landmark_response.json()

number_landmarks = len(landmark_dict["businesses"])
y=0
landmark_search_zip = []
landmark_name = []
landmark_rating = []
landmark_address = []
landmark_display_address = []
landmark_city = []
landmark_zip_code = []
landmark_phone = []
landmark_img = []
landmark_latitude = []
landmark_longitude = []

for y in range(number_landmarks):
    landmark_search_zip.append(f'{input_lat},{input_lon}')
    landmark_name.append(landmark_dict['businesses'][y]['name'])
    landmark_rating.append(landmark_dict['businesses'][y]['rating'])
    landmark_address.append(landmark_dict['businesses'][y]['location']['address1'])
    landmark_city.append(landmark_dict['businesses'][y]['location']['city'])
    landmark_zip_code.append(landmark_dict['businesses'][y]['location']['zip_code'])
    landmark_latitude.append(landmark_dict['businesses'][y]['coordinates']['latitude'])
    landmark_longitude.append(landmark_dict['businesses'][y]['coordinates']['longitude'])
    #display_address.append(rest_dict['businesses'][y]['location']['display_address'])
    landmark_phone.append(landmark_dict['businesses'][y]['phone'])
    landmark_img.append(landmark_dict['businesses'][y]['image_url'])

#print(landmark_dict)

#Create dictionary for dataframe
yelp_landmark_dict = {
'Search Area': landmark_search_zip,
'Name':landmark_name,
'Rating':landmark_rating,
'Address':landmark_address,
'City':landmark_city,
'Zip Code':landmark_zip_code,
'Phone':landmark_phone,
'Image':landmark_img,
'Latitude':landmark_latitude,
'Longitude':landmark_longitude 
}


yelp_landmark_data = pd.DataFrame(yelp_landmark_dict)

#print(yelp_landmark_data)

#--------------------------------------------

#arts 

art_params = {'categories': 'arts',
          'latitude': input_lat,
          'longitude': input_lon,
          'limit': 25
          }

art_response = requests.get(url, headers=headers, params=art_params, timeout=20)

art_dict = art_response.json()

number_arts = len(art_dict["businesses"])
y=0
art_search_zip = []
art_name = []
art_rating = []
art_address = []
art_display_address = []
art_city = []
art_zip_code = []
art_phone = []
art_img = []
art_latitude = []
art_longitude = []

for y in range(number_arts):
    art_search_zip.append(f'{input_lat},{input_lon}')
    art_name.append(art_dict['businesses'][y]['name'])
    art_rating.append(art_dict['businesses'][y]['rating'])
    art_address.append(art_dict['businesses'][y]['location']['address1'])
    art_city.append(art_dict['businesses'][y]['location']['city'])
    art_zip_code.append(art_dict['businesses'][y]['location']['zip_code'])
    art_latitude.append(art_dict['businesses'][y]['coordinates']['latitude'])
    art_longitude.append(art_dict['businesses'][y]['coordinates']['longitude'])
    #display_address.append(rest_dict['businesses'][y]['location']['display_address'])
    art_phone.append(art_dict['businesses'][y]['phone'])
    art_img.append(art_dict['businesses'][y]['image_url'])

#print(art_dict)

#Create dictionary for dataframe
yelp_art_dict = {
'Search Area': art_search_zip,
'Name':art_name,
'Rating':art_rating,
'Address':art_address,
'City':art_city,
'Zip Code':art_zip_code,
'Phone':art_phone,
'Image':art_img,
'Latitude':art_latitude,
'Longitude':art_longitude 
}


yelp_art_data = pd.DataFrame(yelp_art_dict)

yelp_data.to_csv('restaurant_data.csv', index=False)
entry_data.to_csv('entry_data.csv', index=False)

#print(entry_data)
#print(yelp_data)
#print(yelp_bar_data)
#print(yelp_hotel_data)
#print(yelp_gym_data)
#print(yelp_landmark_data)
#print(yelp_art_data)

