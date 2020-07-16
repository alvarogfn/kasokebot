import tweepy
from os import environ
from time import sleep
import functions
from datetime import datetime

class kasokebot(tweepy.StreamListener):
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACESS_KEY, ACESS_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.loop = 0
        
    def streaming(self, track):
        stalking = tweepy.Stream(auth=self.api.auth, listener=self)
        stalking.filter(track=track) 
    
    def on_status(self, status):
        rt_test = functions.no_text(status.text)      
        if rt_test('RT'):
            self.id_tweet = status.id
            self.loop += 1                              # Number of processes done
            print(f'{self.loop}º tweet tracked!')
            return False
        
    def retweet(self):
        try:
            self.api.retweet(self.id_tweet)
        except tweepy.RateLimitError:
            print(f'    Retweet limit exceeded!')   
        except:
            print(f'    Retweet failed!')
        else:         
            print(f'    Retweet done!')
    
    def favorite(self):
        try: 
            self.api.create_favorite(self.id_tweet)
        except tweepy.RateLimitError:
            print(f'    Favorite limit exceeded!')    
        except:
            print(f'    Favorite failed!')   
        else:         
            print(f'    Favorite done!')
            
    def on_error(self, status_code):
        if status_code == 420:
            print('> Bot paused for 15 minutes! <')
            sleep(900)
            return False

print('Start main script!')

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']     # Get environment variables
ACESS_KEY = environ['ACESS_KEY']
ACESS_SECRET = environ['ACESS_SECRET']

narubot = kasokebot(CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET)

tracker = ['Dattebayo', 'Dattebayo!']  

fav_limit = 100                     
ret_limit = 100         # Declaring execution limit variables

while True:
    narubot.streaming(tracker)
    sleep(1)
    if ret_limit > 0:
        narubot.retweet()           # Retweeting    
        ret_limit -= 1
        sleep(1)

    if fav_limit > 0:
        narubot.favorite()          # Favoring
        fav_limit -= 1
        sleep(1)
        
    if datetime.now().hour == 0:                        # Resetting the operations limit
        print('> Reset actions limit! <')
        ret_limit = 100
        fav_limit = 100
