import geopy

import datetime
import io, sys, os
import tweepy
import json
import keys
import pygame, random

geolocator = geopy.geocoders.Nominatim(user_agent="help err plz")

####----TWEEPY SETUP----####

auth = tweepy.OAuthHandler(keys.API_KEY[0], keys.API_KEY[1])
auth.set_access_token(keys.ACCESS_TOKEN[0],keys.ACCESS_TOKEN[1])
word = tweepy.API(auth)
cities = ['Greenville, SC', 'Washington,DC', 'Tampa, FL', 'Moscow, Russia']
dist_mult = [720, 360]

RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,255,0)


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            loc = status._json['user']['location']
            if loc != None:
                try:
                    cities.append(loc)
                    # print(type(loc))
                    # print(loc)
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
    
    processing = False
    locations = []
    print(cities)
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"
    win = pygame.display.set_mode((1440, 720))    
    fps = 60
    fpsClock = pygame.time.Clock()  

    colors = [RED,YELLOW,BLUE,PURPLE,GREEN]
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
                    l = geolocator.geocode(city)
                    locations.append((l.latitude, l.longitude))
                except:
                    pass
            
                
                
        # with open("locations_coord.txt", "a+") as f: #FOR PUTTING IN A FILE
        #     for location in locations:
        #         f.write(str(location[0]) +","+ str(location[1]) + "\n")
            
        # Draw.
        
        for location in locations:
            pos_y = (((720/2)+location[0])*-1) +720
            pos_x = (1440/2)+location[1]
            
            pygame.draw.rect(win,YELLOW,(pos_x,pos_y,4,4))

        pygame.display.flip()
        fpsClock.tick(fps)

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