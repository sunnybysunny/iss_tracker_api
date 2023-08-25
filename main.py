import requests
import time
import smtplib

# my_email and password
MY_EMAIL: "afakeemail@gmailcom"
PASSWORD: "abc124"

# Hard coded Lat and Long of SLC, UT
MY_LAT = 40.760780
MY_LONG = -111.891045


def current_time():
    """this function gets the current MST using the World Time Api"""
    response = requests.get(url="http://worldtimeapi.org/api/timezone/MST")
    mst_info = response.json()
    mst_time = mst_info["datetime"].split("T")[1].split(".")[0].split(":")
    if int(mst_time[0]) == 0:
        return 24
    return int(mst_time[0])


def iss_close_to(lat, long):
    """ this function tracks the location of the ISS and returns a boolean checking to see if the ISS
    is within + 5 or - 5 degrees of input coordinates"""

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # line 18/19 same at iss_latitude >= lat - 5 and iss_latitude <= + 5
    lat_close = lat - 5 <= iss_latitude <= lat + 5
    long_close = long - 5 <= iss_longitude <= long + 5

    # return boolean True/False
    return lat_close and long_close


def is_night(curr_time, parameters):
    """this function checks to see if it's nigh time at the specified coordinates"""
    response = requests.get("https://api.sunrisesunset.io/json", params=parameters)
    # error handling if anything besides a 200 is returned
    response.raise_for_status()

    data = response.json()

    sunrise = data["results"]["sunrise"].split(" ")[0].split(":")
    sunset = data["results"]["sunset"].split(" ")[0].split(":")

    sunrise_hour = (int(sunrise[0]))
    # sunset will always be PM so 12 hours needs to be added for 24 hour time
    sunset_hour = (int(sunset[0]) + 12)
    night_hours = (24 - sunset_hour) + sunrise_hour
    sr = night_hours + sunset_hour
    return curr_time > sunset_hour and curr_time < sr


my_params = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "date": "today",
}


def every_minute():
    tracking = True
    while tracking:
        time.sleep(60)
        if iss_close_to(MY_LAT, MY_LONG) and is_night(current_time(), my_params):
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(MY_EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject: Look Up!\n\n The ISS is in the sky!"
            )
            print("email sent")
        else:
            print("No ISS right now")
            tracking = False

every_minute()
