import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude
MY_EMAIL = "your email"
MY_PASSWORD = "your password"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])
print(iss_latitude)
print(iss_longitude)


#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
print(sunset, sunrise)
time_now = datetime.now()
current_hour = int(time_now.hour)

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


def is_dark(time):
    if sunrise < time < sunset:
        return False
    else:
        return True


def is_close(latitude, longitude):
    if iss_latitude - 5 <= latitude <= iss_latitude + 5 and iss_longitude - 5 <= longitude <= iss_longitude + 5:
        return True


def send_letter():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="email",
                            msg=f"Subject: The ISS is just above you\n\n Look up the sky ! "
                                f"The ISS is there:\nlatitude: {iss_latitude}\nLongitude: {iss_longitude}")

while True:
    time.sleep(60)
    if is_dark(current_hour) and is_close(MY_LAT, MY_LONG):
        send_letter()






