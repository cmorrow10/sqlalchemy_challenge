#### Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

##### Part 1: Analyze and Explore the Climate Data
##### - Precipitation Analysis
##### - Station Analysis

##### Part 2: Design Your Climate App
##### 1. /
##### -Start at the homepage.
##### -List all the available routes.

##### 2. /api/v1.0/precipitation
##### -Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
##### -Return the JSON representation of your dictionary.

##### 3. /api/v1.0/stations
##### -Return a JSON list of stations from the dataset.

##### 4. /api/v1.0/tobs
##### -Query the dates and temperature observations of the most-active station for the previous year of data.
##### -Return a JSON list of temperature observations for the previous year.

##### 5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
##### -Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
##### -For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
##### -For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
