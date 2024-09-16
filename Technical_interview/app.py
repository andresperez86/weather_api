from flask import Flask, request, jsonify
import requests
import sqlite3


app = Flask(__name__)

# Your free wather API key
API_KEY = "6b73e12f8849f37ffcb555973e9a1ab2"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}"
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"

#SQLite DataBase setup
DATABASE = "weather.db"

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    #conn = con.cursor()
    return conn

# Create the tables if they do not exist
def create_tables():
    try:
        conn = get_db_connection()
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS cities (
                                      city_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                      city_name TEXT NOT NULL,
                                      state TEXT,
                                      country TEXT NOT NULL
                                  )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS weather_requests (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                   city_id INTEGER,
                                   status TEXT,
                                   response TEXT,
                                   FOREIGN KEY(city_id) REFERENCES cities(city_id)
                               )''')
    except sqlite3.ProgrammingError as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection closed.")

create_tables()

# Function to fetch city coordinates from OpenWeatherMap
def get_city_coordinates(city, state, country, api_key, limit=1):
    url = f"{BASE_GEO_URL}?q={city},{state},{country}&limit={limit}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            city_data = data[0]
            return {
                'city': city_data['name'],
                'country': city_data['country'],
                'latitude': city_data['lat'],
                'longitude': city_data['lon']
            }
        else:
            return {'error': f"No data found for {city}, {state}, {country}."}
    else:
        return {'error': f"Failed to retrieve data. HTTP Status code: {response.status_code}"}

# Function to fetch weather data based on coordinates


def get_weather_by_coordinates(lat, lon, api_key):
    url = f"{BASE_WEATHER_URL}?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather_info
    else:
        return {'error': f"Failed to retrieve weather data. HTTP Status code: {response.status_code}"}


# wheater end point
@app.route('/weather/<int:city_id>', methods=['GET'])
def get_weather(city_id):
    conn = get_db_connection()
    city = conn.execute('SELECT * FROM cities WHERE city_id = ?', (city_id,)).fetchone()
    if city is None:
        return jsonify({'error': 'City not found'}), 404

    coordinates = get_city_coordinates(city['city_name'], city['state'], city['country'], API_KEY)

    if 'error' in coordinates:
        return jsonify(coordinates), 404

    weather_data = get_weather_by_coordinates(coordinates['latitude'], coordinates['longitude'], API_KEY)

    if 'error' in weather_data:
        conn.execute('INSERT INTO weather_requests (city_id, status, response) VALUES (?, ?, ?)',
                     (city_id, 'failure', str(weather_data)))
        conn.commit()
        return jsonify(weather_data), 500

    conn.execute('INSERT INTO weather_requests (city_id, status, response) VALUES (?, ?, ?)',
                 (city_id, 'success', str(weather_data)))
    conn.commit()

    conn.close()
    return jsonify(weather_data)


# History endpoint
@app.route('/history', methods=['GET'])
def get_history():
    conn = get_db_connection()
    history = conn.execute('''
        SELECT wr.timestamp, c.city_name, wr.response
        FROM weather_requests wr
        JOIN cities c ON wr.city_id = c.city_id
        WHERE wr.status = 'success'
        ORDER BY wr.timestamp DESC
        LIMIT 5
    ''').fetchall()

    result = [{'timestamp': row['timestamp'], 'city': row['city_name'], 'weather': row['response']} for row in history]
    print(result)
    conn.close()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)







