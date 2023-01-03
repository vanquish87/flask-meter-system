Live Building Systems 2018
Coding Challenge - Part 1/2 Back End:
Goal: Spin up a basic Flask application, connect it to a local SQLite database, add fake meter
data to the db, then implement a RESTful application for displaying the fake meter data in .json
format.
DB Schema:
Table: : ”meters”
Fields:
“id”: Int - Primary Key
“label”: String - name of meter
Table: “meter_data”
Fields:
“id”: Int - Primary Key
“meter_id”: Int - foreign key to associate MeterData entry to specific Meter
“timestamp”: python DateTime object - timestamp of meter_data entry
“value”: int - represents the value we are storing for a specific time for that meter

The application should be able to respond to the following queries:
Endpoint: /meters/
Should display a list of the unique meters in the DB. Each one should be a clickable link
that then points to the meter’s .json page that displays all of it’s associate data. So if I click on
the “Meter X” link it should point to the /meters/x/ url/endpoint.
Endpoint: /meters/{METER_ID}
Should display a list sorted by timestamp of all the datapoint entries from the meter_data
in json format for the specific meter_id passed into the URL as a parameter.