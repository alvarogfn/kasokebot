import tweepy
from os import environ
from time import sleep
import functions
from random import randint, choice

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
            print(f'    Re-tweet!.')
    
    def favorite(self, tweet_id):
        
        try: 
            self.api.create_favorite(tweet_id)
        
        except tweepy.RateLimitError:
            print(f'    Limite de favoritos exedido.')
            
        except Exception as error:
            print(f'    Não foi possível favoritar.\nERROR = [{error}]')
        
        else:         
            print(f'    Tweet favoritado!.')
    
    def replying(self, tweet_id, user_name):
        
        emojis = choice(['^^', '^-^', ':3', '*-*', '>-<', '>_<', '<_<', '>_>', 'o-o', 'u_u'])
        
        img = f'images/dattebayo{randint(0, 3)}.gif'
        
        try:
            self.api.update_with_media(status=f'@{user_name} Baayo!!! {emojis}', in_reply_to_status_id=tweet_id, filename=img)
        except tweepy.RateLimitError:
            print(f'    Limite de favoritos exedido.')
            
        except Exception as error:
            print(f'    Não foi possível responder.\nERROR = [{error}]')
        
        else:         
            print(f'    Tweet respondido!.')
    
    def update_status(self, text):
        try:
            self.api.update_status(text)
            
        except tweepy.RateLimitError:
            print(f'    Limite de status exedido.')
            
        except Exception as error:
            print(f'    Não foi possível tweetar.\nERROR = [{error}]')
        
        else:         
            print(f'    Tweet feito!.')


print('Start NaruBot!')

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACESS_KEY = environ['ACESS_KEY']
ACESS_SECRET = environ['ACESS_SECRET']

narubot = narubot(CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET)

loop = 1
freshing_update_status = 60
tracker = ['Dattebayo', 'Dattebayo!']

while True:
    while True:
        narubot.streaming(tracker)
        if narubot.status:
            break

        print(f'{loop}º tweet tracked!')
        sleep(1)
        
        narubot.replying(narubot.informations['tweet_id'], narubot.informations['user_name'])
        sleep(1)
        
        narubot.retweet(narubot.informations['tweet_id'])
        sleep(1)
        
        narubot.favorite(narubot.informations['tweet_id'])
        sleep(1)
            
        loop += 1
        
        sleep(1)
    print('NaruBot desligado por 5 minutos!')
    sleep(300)