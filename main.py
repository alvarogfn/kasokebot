import tweepy
from os import environ
from time import sleep
import functions
from random import randint, choice
from datetime import datetime

class narubot(tweepy.StreamListener):
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
            text_tweet = status.text
            id_tweet = status.id
            user = status.user.id
            screen_name = status.user.screen_name
            
            self.informations = {"tweet": text_tweet, "tweet_id": id_tweet, "user_id": user, "user_name": screen_name}
            
            return False

    def on_error(self, status_code):
        if status_code == 420:
            self.status = True
            return False


    def following(self, user_name):
        pass
    
    def retweet(self, tweet_id):
        
        try:
            self.api.retweet(tweet_id)
            
        except tweepy.RateLimitError:
            print(f'    Limite de retweets exedido.')
            
        except Exception as error:
            print(f'    Não foi possível retweetar.\nERROR = [{error}]')
        
        else:         
            print(f'    Re-tweet!')
    
    def favorite(self, tweet_id):
        
        try: 
            self.api.create_favorite(tweet_id)
        
        except tweepy.RateLimitError:
            print(f'    Limite de favoritos exedido.')
            
        except Exception as error:
            print(f'    Não foi possível favoritar.\nERROR = [{error}]')
        
        else:         
            print(f'    Tweet favoritado!')
    
    def replying(self, tweet_id, user_name):
        pass
    
    def update_status(self, text):
        pass


print('Start NaruBot!')

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACESS_KEY = environ['ACESS_KEY']
ACESS_SECRET = environ['ACESS_SECRET']

narubot = narubot(CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET)

loop = 1
fav_limit = 100
ret_limit = 100

tracker = ['Dattebayo', 'Dattebayo!']

while True:
    while True:
        narubot.streaming(tracker)
        if narubot.status:
            break

        print(f'{loop}º tweet tracked!')
        sleep(1)
        
        if ret_limit > 0:
            narubot.retweet(narubot.informations['tweet_id'])
            sleep(1)
            ret_limit -= 1

        if fav_limit > 0:
            narubot.favorite(narubot.informations['tweet_id'])
            sleep(1)
            fav_limit -= 1
        
        if datetime.now().hour == 0:
            ret_limit = 100
            fav_limit = 100
        
        sleep(1)
    print('NaruBot desligado por 15 minutos!')
    sleep(900)