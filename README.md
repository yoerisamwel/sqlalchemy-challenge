Readme
 
This project was part of the GWU bootcamp. This part of the course was focused on getting a solid understanding of SQLAlchemy a python library used to interact with SQL databases. Expanding the SQL project we conducted last week.
 
The project consisted of two part one was connecting to the database and analyse the data in a Jupiter notebook. The main focus in the notebook was to pull the data from the created SQLAlchemy database and process and analyze the data. The second section was to setup a API for users to pull the analysis from.
 
Instructions section 1:
Analyze and Explore the Climate Data
In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:
1.	Note that you’ll use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete your climate analysis and data exploration.
2.	Use the SQLAlchemy create_engine() function to connect to your SQLite database.
3.	Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.
4.	Link Python to the database by creating a SQLAlchemy session.
 
Instructions section 2
 
Design Your Climate App
Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:
1.	/
o	Start at the homepage.
o	List all the available routes.
2.	/api/v1.0/precipitation
o	Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
o	Return the JSON representation of your dictionary.
3.	/api/v1.0/stations
o	Return a JSON list of stations from the dataset.
4.	/api/v1.0/tobs
o	Query the dates and temperature observations of the most-active station for the previous year of data.
o	Return a JSON list of temperature observations for the previous year.
5.	/api/v1.0/<start> and /api/v1.0/<start>/<end>
o	Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
o	For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
o	For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
 
 
The script is setup in the following sections:
1.	Importing the libraries needed.
We used Flask/SQLAlchemy, Flask and Pandas for this exercise. I attached a requirements file showing the versions of the libraries used.
2.	Connection to the database
We setup a SQL lite database in which we stored the datasets needed for this exercise. In the database setup section I pulled the data and setup the connection with the database.
3.	Functions
I placed all the logic in functions which are called in the app.routes. In a future version this would allow me to expand the UI and reuse these functions whenever possible.
4.	Website setup
The UI for this project was written in HTML and some CSS was added. This UI provides the consumer of the data with he option to export parts of the project dataset. For this example the user can export the precipitation and the len/lon/elevation per weather station as well as the temperature.
--------need to add context
5.	The last two app.route function are to capture the start and end date as well as a function to validate if this is an actual valid date entered by the consumer.
For the Javascript used in the website I used a example I found in Stackoverflow.
•	userhttps://stackoverflow.com/questions/41216153/javascript-error-object-htmlinputelementobject-htmlinputelement
