import datetime
import io
import json
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
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
cities = []#'Greenville, SC', 'Washington,DC', 'Tampa, FL', 'Moscow, Russia']
locations = {} #json formatter plz yes
location_coords = []

dist_mult = [720, 360] #used later for drawing on the map

RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255, 0, 255)
WHITE = (255,255,255)
BLACK = (0,0,0)


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

    pass_in_json() #curr database of locations
    print(cities)
    for city in cities:
        if len(cities) > 0:
            #print(city)
            if city:
                try:
                    if city in locations:
                        #print("city in locations")
                        location_coords.append((locations[str(city)]['lat'],locations[str(city)]['long']))
                        
                    else:
                        #print("City not in locations")
                        format_json(locations, str(city), None, None) #prepare for non-existant city
                        l = geolocator.geocode(city)
                        if l.latitude and l.longitude:
                            location_coords.append((l.latitude, l.longitude))

                        if l.latitude: #if city DOES infact exist, overwrite
                            del locations[city]
                            format_json(locations, str(city), l.latitude, l.longitude)

                except Exception as e:
                    print(e)

    write_json(locations)


def draw_loc():
    locs = []
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"
    win = pygame.display.set_mode((1440, 720))    
    fps = 60
    fpsClock = pygame.time.Clock()  

    mapImg = pygame.image.load("img/map.jpg")
    mapImg = pygame.transform.scale(mapImg, (1440,720))


    while True:
        win.fill((0, 0, 0))
        win.blit(mapImg,(0,0))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Update.
        if len(location_coords) > 0:
            locs.append(location_coords.pop())
            time.sleep(.2)
        else:
            pygame.draw.rect(win,BLACK,(0,0,4,4))    #locations are processed
                
        
        for location in locs:
            if location[0] and location[1]:
                pos_y = (((720/2) + 4*location[0]) * -1) + 720
                pos_x = (1440/2) + 4*location[1] 
                
            
            pygame.draw.rect(win,RED,(pos_x-2,pos_y-2,4,4))
        
        pygame.display.flip()
        fpsClock.tick(fps)

def launch_stream():
    global sTime #start time
    sTime = datetime.datetime.now()
    myStreamListener = MyStreamListener() 
    myStream = tweepy.Stream(auth = word.auth, listener = myStreamListener)
    myStream.filter(follow = ['25073877'], is_async = False) #Best solution.
    

def write_json(data): # format of "{ cities: [ {cityname: cityname, lat: lat, long: long},...] }"
    with io.open("locations.json", "w+") as f:
        json.dump(data, f, indent = 4)

def format_json(data, city, lat, lon): #add to list to be written to the json in write_json
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
    except: #empty list
        pass
    



launch_stream()

proc_loc()

draw_loc()




