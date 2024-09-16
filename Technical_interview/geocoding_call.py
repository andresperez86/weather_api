import requests


def get_city_coordinates(city, state, country, api_key, limit=1):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit={limit}&appid={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            city_data = data[0]
            print(f"City: {city_data['name']}, Country: {city_data['country']}")
            print(f"Latitude: {city_data['lat']}, Longitude: {city_data['lon']}")
        else:
            print(f"No data found for {city}, {state}, {country}.")
    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")


# Replace 'your_api_key' with your actual OpenWeatherMap API key

api_key = '6b73e12f8849f37ffcb555973e9a1ab2'

# Example of calling the function
get_city_coordinates(city='Los Angeles', state='CA', country='US', api_key=api_key)



