# Climate Analysis and Flask API Project

This project involves analyzing climate data from Honolulu, Hawaii using Python, SQLAlchemy, Pandas, and Matplotlib. It includes a Flask API to access various endpoints for retrieving climate data.

## Overview

The project aims to perform comprehensive climate analysis on historical data collected from Honolulu, Hawaii. It explores precipitation patterns, temperature trends, and provides insights into weather station information. A Flask API is implemented to facilitate easy access to the analyzed data through specific endpoints.

## Flask API Endpoints

### `/api/v1.0/precipitation`

- Retrieves the last 12 months of precipitation data.
- Returns a JSON representation of precipitation data with date as the key and prcp as the value.

### `/api/v1.0/stations`

- Retrieves a JSON list of weather stations from the dataset.

### `/api/v1.0/tobs`

- Retrieves temperature observations for the previous year from the most active station.
- Returns a JSON list of temperature observations (TOBS) for the previous year.

### `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

- Retrieves minimum, average, and maximum temperatures for a specified start date or start-end date range.
- Returns a JSON object with TMIN, TAVG, and TMAX values.

## Notes

- **Database**: The project utilizes a SQLite database (`hawaii.sqlite`) for storing and querying climate data.
- **Dependencies**: Python 3.x, Flask, SQLAlchemy, Pandas, and Matplotlib.
- **Session Handling**: Close SQLAlchemy sessions after use to prevent memory leaks.

