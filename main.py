import requests
import time
from datetime import datetime
from smtplib import SMTP

# Hard coded Lat and Long of SLC, UT
MY_LAT = 40.760780
MY_LONG = -111.891045


def get_coordinates(latitude, longitude):
    pass


def iss_close_to(lat, long):
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # line 18/19 same at iss_latitude >= lat - 5 and iss_latitude <= + 5
    lat_close = lat - 5 <= iss_latitude <= lat + 5
    long_close = long - 5 <= iss_longitude <= long + 5

    # Test
    # lat_close = iss_latitude
    # long_close = iss_longitude

    # line 21 will return boolean True/False
    return lat_close and long_close


my_params = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "date": "today",
}

def is_night(parameters):
    response = requests.get("https://api.sunrisesunset.io/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data["results"]["sunrise"].split(" ")
    sunset = data["results"]["sunset"].split(" ")
    print(sunrise)
    print(sunset)
    # sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    # sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # return curr_time > sunset and curr_time < sunrise

is_night(my_params)

def every_minute():
    while True:
        if iss_close_to(MY_LAT, MY_LONG) and is_night(my_params):
            print("email sent: LOOK UP!")
            time.sleep(60)





