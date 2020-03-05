from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="TestApp")



locations = ["Madison WC", "Lincoln NB", "Greenville, SC", "Greenville NC"]
for i in locations:
    location = geolocator.geocode(i)
    print((location.latitude, location.longitude))