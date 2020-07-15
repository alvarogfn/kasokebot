import tweepy
from os import environ
from time import sleep
import functions
from random import randint, choice
from datetime import datetime

class kasokebot(tweepy.StreamListener):
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACESS_KEY, ACESS_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.status = False
        
    def streaming(self, track):
        stalking = tweepy.Stream(auth=self.api.auth, listener=self)
        stalking.filter(track=track) 
    
    def on_status(self, status):
        rt_test = functions.no_text(status.text)
        
        if rt_test('RT'):   
            id_tweet = status.id
            user = status.user.id
            screen_name = status.user.screen_name
            self.informations = {"tweet_id": id_tweet, "user_id": user, "user_name": screen_name}
            return False

    def on_error(self, status_code):
        if status_code == 420:
            self.status = True
            return False
    
    def retweet(self, tweet_id):
        try:
            self.api.retweet(tweet_id)
        except tweepy.RateLimitError:
            print(f'    Retweet limit exceeded!')   
        except:
            print(f'    Retweet failed!')
        else:         
            print(f'    Retweet done!')
    
    def favorite(self, tweet_id):
        try: 
            self.api.create_favorite(tweet_id)
        
        except tweepy.RateLimitError:
            print(f'    Favorite limit exceeded!')    
        except:
            print(f'    Favorite failed!')   
        else:         
            print(f'    Favorite done!')


print('Start main script!')

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']        # Get environment variables
ACESS_KEY = environ['ACESS_KEY']
ACESS_SECRET = environ['ACESS_SECRET']

narubot = kasokebot(CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET)

fav_limit = 100                     
ret_limit = 100                                 # Declaring execution limit variables

tracker = ['Dattebayo', 'Dattebayo!']

loop = 1    #Number of processes done

while True:
    narubot.status == False                 # Declaring error status as false
    
    while True:
        
        narubot.streaming(tracker)
        
        if narubot.status:
            break

        print(f'{loop}º tweet tracked!')
        sleep(1)
        
        if ret_limit > 0:
            narubot.retweet(narubot.informations['tweet_id'])           # Retweeting
            sleep(1)
            ret_limit -= 1

        if fav_limit > 0:
            narubot.favorite(narubot.informations['tweet_id'])          # Favoring
            sleep(1)
            fav_limit -= 1
        
        if datetime.now().hour == 0:                        # Resetting the operations limit
            ret_limit = 100
            fav_limit = 100
        
        sleep(1)
    print('>>>>>>>>>>>> Paused for 15 minutes! <<<<<<<<<<<<<<')             # Pause
    sleep(900)