import requests
def get_weather(city:str):
    city_clean = city.strip()
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_clean}&count=1&language=en&format=json"
    try:
        geo_response = requests.get(geocode_url,timeout=10)
        geo_response.raise_for_status()
        geo_data =  geo_response.json()

        if not geo_data.get("results"):
            return {"error": f"Could not find coordinates for city: '{city_clean}'"}

        location_result = geo_data["results"][0]
        lat = location_result["latitude"]
        lon = location_result["longitude"]
        resolved_name = location_result.get("name", city_clean)
        country = location_result.get("country", "")

        # Step 2: Fetch current weather using the coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&wind_speed_unit=ms"

        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current_data = weather_data.get("current", {})

        return {
            "city": resolved_name,
            "country": country,
            "latitude": lat,
            "longitude": lon,
            "temperature": f"{current_data.get('temperature_2m')}°C",
            "unit": "Celsius"
        }

    except requests.exceptions.RequestException as exc:
        return {"error": f"Network error while fetching weather data: {exc}"}
    except Exception as exc:
        return {"error": f"An unexpected error occurred: {exc}"}