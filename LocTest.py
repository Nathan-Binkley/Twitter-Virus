from geopy.geocoders import Nominatim
import threading
import datetime
import io
import tweepy
import json
import keys
geolocator = Nominatim(user_agent="TestApp")

####----TWEEPY SETUP----####

auth = tweepy.OAuthHandler(keys.API_KEY[0], keys.API_KEY[1])
auth.set_access_token(keys.ACCESS_TOKEN[0],keys.ACCESS_TOKEN[1])
word = tweepy.API(auth)
cities = []

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            loc = status._json['user']['location']
            if loc != None:
                try:
                    cities.append(loc)
                    print("Appending: " + loc)
                except: 
                    pass
        except:
            pass
        if datetime.datetime.now() - sTime >=  datetime.timedelta(hours=0, minutes=0, seconds=10):
            return False

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            print(status_code)

def proc_loc():
    locations = []
    print(cities)
    for city in cities:
        if city:
            try:
                location = geolocator.geocode(city)
                print("New LOC: " + location)
                locations.append((location.latitude, location.longitude))
                print("Successful Append")
            except:
                print("Err")
            
    with open("locations_coord.txt", "w+") as f:
        for location in locations:
            print("Writing " + location)
            f.write(location + "\n")

def launch_stream():
    global sTime
    sTime = datetime.datetime.now()
    myStreamListener = MyStreamListener() 
    myStream = tweepy.Stream(auth = word.auth, listener = myStreamListener)
    myStream.filter(follow = ['25073877'], is_async = False) #Best solution.
    

# with open("locations.txt","w+") as f: #Wipe the file
#     f.truncate()
# t2 = threading.Thread(target=proc_loc,args=())
# t2.start()
# t2.join()



launch_stream()
proc_loc()

