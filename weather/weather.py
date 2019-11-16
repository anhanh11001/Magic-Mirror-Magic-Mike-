import http.client
import json
from datetime import datetime

API_KEY = "21c1e3f90emshcc4b4414581151dp1741b7jsnef8d24881752"
API_HOST = "community-open-weather-map.p.rapidapi.com"

class Weather:
    def __init__(self):
        self.location = "Enschede"
        self.temp_current = 0
        self.temp_max = 0
        self.temp_min = 0
        self.weather_description = "No description available"
        self.humidity = 0
        self.pressure = 0
        self.visibility = 0
        self.wind_speed = 0
        self.sunrise = 0
        self.sunset = 0

        self.update_weather()

    def __str__(self):
        description = """The current weather in {} is:
        Current Temperature: {} °C
        Weather Description: {}
        Pressure: {} mb
        Visibility: {} km
        Wind Speed: {} km/h
        Sunrise Time: {}
        Sunset Time: {}
        """.format(self.location, self.temp_current, self.weather_description, self.pressure,
                   self.visibility, self.wind_speed, self.sunrise, self.sunset)

        return description

    def update_weather(self):
        data = self.get_weather_data()
        if data is not None:
            weather_dict = json.loads(data)
            main = weather_dict['weather'][0]
            weather = weather_dict['main']

            self.temp_current = round(self.get_cel_temp(weather['temp']), 1)
            self.temp_max = round(self.get_cel_temp(weather['temp_max']), 1)
            self.temp_min = round(self.get_cel_temp(weather['temp_min']), 1)
            self.weather_description = main['main']
            self.weather_id = main['id']
            self.humidity = weather['humidity']
            self.pressure = weather['pressure']
            self.visibility = float(weather_dict['visibility']) / 1000  # km
            self.wind_speed = float(weather_dict['wind']['speed'])  # km/h
            self.sunrise = self.get_time(weather_dict['sys']['sunrise'])
            self.sunset = self.get_time(weather_dict['sys']['sunset'])

    def get_weather_data(self):
        # conn = http.client.HTTPSConnection(API_HOST)
        #
        # headers = {
        #     'x-rapidapi-host': API_HOST,
        #     'x-rapidapi-key': API_KEY
        # }
        #
        # conn.request("GET",
        #              "/weather?callback=test&id=2172797&units=%22metric%22%20or%20%22imperial%22&mode=xml%2C%20html&q=" + self.location,
        #              headers=headers)
        #
        # res = conn.getresponse()
        # data = res.read().decode("utf-8").strip("test(").strip(")")

        data = "{\"coord\":{\"lon\":-0.13,\"lat\":51.51},\"weather\":[{\"id\":804,\"main\":\"Clouds\",\"description\":\"overcast clouds\",\"icon\":\"04d\"}],\"base\":\"stations\",\"main\":{\"temp\":280.72,\"pressure\":1016,\"humidity\":100,\"temp_min\":278.15,\"temp_max\":283.71},\"visibility\":8000,\"wind\":{\"speed\":1},\"rain\":{},\"clouds\":{\"all\":100},\"dt\":1571820595,\"sys\":{\"type\":1,\"id\":1414,\"country\":\"GB\",\"sunrise\":1571812642,\"sunset\":1571849528},\"timezone\":3600,\"id\":2643743,\"name\":\"London\",\"cod\":200}"
        return data

    @staticmethod
    def get_cel_temp(temp):
        return temp - 273.15

    @staticmethod
    def get_time(unix_time):
        return datetime.utcfromtimestamp(int(unix_time)).strftime('%H:%M:%S')


if __name__ == '__main__':
    w = Weather()
    print(w)
