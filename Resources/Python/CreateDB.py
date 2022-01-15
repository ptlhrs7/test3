import sqlalchemy as sql
from sqlalchemy_utils import database_exists, create_database
from api_keys import password, yelp_key

def create_db(): 
    try:
        engine = sql.create_engine(f"postgresql://postgres:{password}@localhost/TravelBuddyDBTest")
        print("Connection to PostgreSQL successful.")
        if not database_exists(engine.url):
            create_database(engine.url)
            print("New database created: TravelBuddyDBTest")
            create_tables(engine)
        else:
            print("TravelBuddyDBTest found.")
    except:
        print("Failed to connect.")

def create_tables(engine):

     with engine.connect():
                engine.execute( 'create table searches\
                    (Loc_Key varchar PRIMARY KEY,\
                    target varchar,\
                    Area text,\
                    City text,\
                    Loc_State text,\
                    Country text,\
                    Input_Date date);\
                    \
                    create table restaurants\
                    (loc_key varchar,\
                    bus_id text,\
                    bus_name varchar,\
                    price text,\
                    rating text,\
                    address text,\
                    city text,\
                    zip_code varchar,\
                    phone varchar,\
                    image varchar,\
                    latitude decimal,\
                    longitude decimal,\
                    primary key (Bus_ID, Loc_Key),\
                    foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE);\
                    \
                    create table bars\
                    (loc_key varchar,\
                    bus_id text,\
                    bus_name varchar,\
                    price text,\
                    rating text,\
                    address text,\
                    city text,\
                    zip_code varchar,\
                    phone varchar,\
                    image varchar,\
                    latitude decimal,\
                    longitude decimal,\
                    primary key (Bus_ID, Loc_Key),\
                    foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE);\
                    \
                    create table hotels\
                    (loc_key varchar,\
                    bus_id text,\
                    bus_name varchar,\
                    price text,\
                    rating text,\
                    address text,\
                    city text,\
                    zip_code varchar,\
                    phone varchar,\
                    image varchar,\
                    latitude decimal,\
                    longitude decimal,\
                    primary key (Bus_ID, Loc_Key),\
                    foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE);\
                    \
                    create table gyms\
                    (loc_key varchar,\
                    bus_id text,\
                    bus_name varchar,\
                    price text,\
                    rating text,\
                    address text,\
                    city text,\
                    zip_code varchar,\
                    phone varchar,\
                    image varchar,\
                    latitude decimal,\
                    longitude decimal,\
                    primary key (Bus_ID, Loc_Key),\
                    foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE);\
                    \
                    create table landmarks\
                    (loc_key varchar,\
                    bus_id text,\
                    bus_name varchar,\
                    price text,\
                    rating text,\
                    address text,\
                    city text,\
                    zip_code varchar,\
                    phone varchar,\
                    image varchar,\
                    latitude decimal,\
                    longitude decimal,\
                    primary key (Bus_ID, Loc_Key),\
                    foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE);\
                    \
                    create table arts\
                    (loc_key varchar,\
                    bus_id text,\
                    bus_name varchar,\
                    price text,\
                    rating text,\
                    address text,\
                    city text,\
                    zip_code varchar,\
                    phone varchar,\
                    image varchar,\
                    latitude decimal,\
                    longitude decimal,\
                    primary key (Bus_ID, Loc_Key),\
                    foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE);')

#create_db()