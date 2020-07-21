import tweepy
from os import environ
from time import sleep
from functions import no_text, tweets_track, time_for_sleep
from datetime import datetime

class kasokebot(tweepy.StreamListener):
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACESS_KEY, ACESS_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
         
    def streaming(self, track): 
        stalking = tweepy.Stream(auth=self.api.auth, listener=self)
        stalking.filter(track=track) 
    
    def on_status(self, status):
        self.status = True
        rt_test = no_text(status.text)    
        if rt_test('RT'):
            loop = tweets_track() 
            self.id_tweet = status.id
            print(f'{loop}º tweet tracked!') # Number of processes done
            return False
        
    def retweet(self):
        try:
            self.api.retweet(self.id_tweet)
            print(end='')
        except tweepy.RateLimitError:
            print('    Retweet limit exceeded.')
            return True
        except:
            print('    Retweet failed.')
        else:         
            print('    Retweet done.')
            return False 
    
    def favorite(self):
        try: 
            self.api.create_favorite(self.id_tweet)
            print(end='')
        except tweepy.RateLimitError:
            print('    Favorite limit exceeded.')
            return True
        except:
            print('    Favorite failed.')   
        else:         
            print('    Favorite done.')
            return False 
            
    def on_error(self, status_code):
        if status_code == 420:
            self.status = False
            print('> Bot paused for 15 minutes! <') 
            sleep(900)
            return False

print('Start main script!')

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']    # Get environment variables
ACESS_KEY = environ['ACESS_KEY']
ACESS_SECRET = environ['ACESS_SECRET']

narubot = kasokebot(CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET)

tracker = ['Dattebayo lang:pt', 'Dattebayo! lang:pt']

retlimit = False
favlimit = False

while True:
    sleep(2)
    narubot.streaming(tracker)
    if narubot.status:
        if not retlimit:
            sleep(1)
            retlimit = narubot.retweet()
        if not favlimit:
            sleep(1)
            favlimit = narubot.favorite()
        while retlimit and favlimit:
            if time_for_sleep() % 60 == 0:
                if time_for_sleep() > 0:
                    seconds = time_for_sleep()
                    hour = int((seconds / 60) / 60)
                    minute = (seconds - hour * 60 * 60) / 60
                    print(f'> {hour:.0f} hours and {minute:.0f} minutes left to reset <')
                    sleep(1)
                else:
                    retlimit = False
                    favlimit = False
                    print('> Reseting <')
                    sleep(1)