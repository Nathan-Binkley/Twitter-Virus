import datetime
import io
import json
import os
import random
import sys
import time

import pygame
import tweepy
import geopy
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

import keys

geolocator = Nominatim(user_agent="specify_your_app_name_here")

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)



####----TWEEPY SETUP----####

auth = tweepy.OAuthHandler(keys.API_KEY[0], keys.API_KEY[1])
auth.set_access_token(keys.ACCESS_TOKEN[0],keys.ACCESS_TOKEN[1])
word = tweepy.API(auth)
cities = ['Greenville, SC', 'Washington,DC', 'Tampa, FL', 'Moscow, Russia']
locations = {} #json formatter plz yes

dist_mult = [720, 360] #used later for drawing on the map

RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255, 0, 255)
WHITE = (255,255,255)


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            loc = status._json['user']['location']
            if loc != None:
                try:
                    cities.append(loc)
                except: 
                    pass
        except:
            pass
        if datetime.datetime.now() - sTime >=  datetime.timedelta(hours=0, minutes=0, seconds=30):
            return False

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            print(status_code)

def proc_loc():
    
    
    location_coords = []
    print(cities)
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"
    win = pygame.display.set_mode((1440, 720))    
    fps = 60
    fpsClock = pygame.time.Clock()  


    while True:
        win.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Update.
        if len(cities) > 0:
            city = cities.pop()
            
            if city:
                try:
                    if city in locations:
                        print("city in locations")
                        location_coords.append((locations[str(city)]['lat'],locations[str(city)]['long']))
                        print("location added to json")
                        time.sleep(.5)
                    else:
                        print("city not in locations")
                        l = geolocator.geocode(city)
                        location_coords.append((l.latitude, l.longitude))
                        format_json(locations, str(city), l.latitude, l.longitude)
                        print("Formatted Json")
                    
                except Exception as e:
                    print(e)
                    
        else:
            pygame.draw.rect(win,WHITE,(0,0,4,4))    
                
                
        
        
        
        
        for location in location_coords:
            pos_y = (((720/2) + 4*location[0]) * -1) + 720
            pos_x = (1440/2) + 4*location[1] 
            
            
            pygame.draw.rect(win,YELLOW,(pos_x,pos_y,4,4))

        write_json(locations)
        
        pygame.display.flip()
        fpsClock.tick(fps)

def launch_stream():
    global sTime #start time
    sTime = datetime.datetime.now()
    myStreamListener = MyStreamListener() 
    myStream = tweepy.Stream(auth = word.auth, listener = myStreamListener)
    myStream.filter(follow = ['25073877'], is_async = False) #Best solution.
    

def write_json(data): # format of 
                                 # { cities: [ {cityname: cityname, lat: lat, long: long},...] }
    with io.open("locations.json", "w") as f:
        json.dump(data, f, indent = 4)

def format_json(data, city, lat, lon):
    data[city] = []
    data[city] = {
        "lat" : lat,
        "long" : lon
    }

def pass_in_json(): # Return list (city name, lat, long) ???
    global locations
    try:
        with open("locations.json", "r") as f:
            locations = json.loads(f.read())
    except:
        pass
    

pass_in_json()



#launch_stream()

proc_loc()






