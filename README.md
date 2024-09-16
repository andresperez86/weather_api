# Weather API

This is a simple weather API that fetches weather data for a set of preset cities using the OpenWeatherMap API.

Setup Instructions

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Set up the SQLite database and run the application:
   
   python app.py
   

API Endpoints

- `/weather/<city_id>`: Get weather data for a city by city ID.
- `/history`: Get the 5 most recent successful weather requests.

Future Improvements

- Implement caching for API responses.
- Add more detailed error handling.
- Add rate limiting to prevent API abuse.


Conclusion
This solution integrates city data retrieval, weather fetching, and request logging using Flask, SQLite, and OpenWeatherMap. You can extend it with additional features such as caching or API rate limiting based on your project requirements.
