create table searches (
Loc_Key varchar PRIMARY KEY,
target varchar,
Area text,
City text,
Loc_State text,
Country text,
Input_Date date
);

create table restaurants (
Loc_Key varchar,
Bus_ID text,
Bus_Name varchar,
Price text,
Rating text,
Address text,
City text,
ZIP_Code varchar,
Phone varchar,
Image varchar,
Latitude decimal,
Longitude decimal,
primary key (Bus_ID, Loc_Key),
foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE
);

create table bars (
Loc_Key varchar,
Bus_ID text,
Bus_Name varchar,
Price text,
Rating text,
Address text,
City text,
ZIP_Code varchar,
Phone varchar,
Image varchar,
Latitude decimal,
Longitude decimal,
primary key (Bus_ID, Loc_Key),
foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE
);

create table hotels (
Loc_Key varchar,
Bus_ID text,
Bus_Name varchar,
Price text,
Rating text,
Address text,
City text,
ZIP_Code varchar,
Phone varchar,
Image varchar,
Latitude decimal,
Longitude decimal,
primary key (Bus_ID, Loc_Key),
foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE
);

create table gyms (
Loc_Key varchar,
Bus_ID text,
Bus_Name varchar,
Price text,
Rating text,
Address text,
City text,
ZIP_Code varchar,
Phone varchar,
Image varchar,
Latitude decimal,
Longitude decimal,
primary key (Bus_ID, Loc_Key),
foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE
);

create table landmarks (
Loc_Key varchar,
Bus_ID text,
Bus_Name varchar,
Price text,
Rating text,
Address text,
City text,
ZIP_Code varchar,
Phone varchar,
Image varchar,
Latitude decimal,
Longitude decimal,
primary key (Bus_ID, Loc_Key),
foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE
);

create table arts (
Loc_Key varchar,
Bus_ID text,
Bus_Name varchar,
Price text,
Rating text,
Address text,
City text,
ZIP_Code varchar,
Phone varchar,
Image varchar,
Latitude decimal,
Longitude decimal,
primary key (Bus_ID, Loc_Key),
foreign key (Loc_Key) references searches(Loc_Key) ON DELETE CASCADE
);