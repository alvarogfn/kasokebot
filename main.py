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

    def on_error(self, status_error):
            if status_error == 420:
                self.status = True
                return False
            

    def following(self, user_name):
        pass
    
    def retweet(self, tweet_id):
        
        try:
            self.api.retweet(tweet_id)
            
        except tweepy.RateLimitError:
            print(f'\033[31m    Limite de retweets exedido.\033[37m')
            
        except Exception as error:
            print(f'\033[31m    Não foi possível retweetar.\nERROR = [{error}]\033[37m')
        
        else:         
            print(f'\033[32m    Re-tweet!.\033[37m')
    
    def favorite(self, tweet_id):
        
        try: 
            self.api.create_favorite(tweet_id)
        
        except tweepy.RateLimitError:
            print(f'\033[31m    Limite de favoritos exedido.\033[37m')
            
        except Exception as error:
            print(f'\033[31m    Não foi possível favoritar.\nERROR = [{error}]\033[37m')
        
        else:         
            print(f'\033[32m    Tweet favoritado!.\033[37m')
    
    def replying(self, tweet_id, user_name):
        
        emojis = choice(['^^', '^-^', ':3', '*-*', '>-<', '>_<', '<_<', '>_>', 'o-o', 'u_u'])
        
        img = f'images\\dattebayo{randint(0, 3)}.gif'
        
        try:
            self.api.update_with_media(status=f'@{user_name} Baayo!!! {emojis}', in_reply_to_status_id=tweet_id, filename=img)
        except tweepy.RateLimitError:
            print(f'\033[31m    Limite de favoritos exedido.\033[37m')
            
        except Exception as error:
            print(f'\033[31m    Não foi possível responder.\nERROR = [{error}]\033[37m')
        
        else:         
            print(f'\033[32m    Tweet respondido!.\033[37m')
    
    def update_status(self, text):
        try:
            self.api.update_status(text)
            
        except tweepy.RateLimitError:
            print(f'\033[31m    Limite de status exedido.\033[37m')
            
        except Exception as error:
            print(f'\033[31m    Não foi possível tweetar.\nERROR = [{error}]\033[37m')
        
        else:         
            print(f'\033[32m    Tweet feito!.\033[37m')


print('Start NaruBot!')

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACESS_KEY = environ['ACESS_KEY']
ACESS_SECRET = environ['ACESS_SECRET']


narubot = narubot(CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET)

loop = 1
freshing_update_status = 0
tracker = ['Dattebayo', 'Dattebayo!']

while True:
    while True:
        narubot.streaming(tracker)
        if narubot.status:
            break

        print(f'\033[33m{loop}º tweet tracked!\033[37m')
        
        narubot.replying(narubot.informations['tweet_id'], narubot.informations['user_name'])
        sleep(0.5)
        
        narubot.retweet(narubot.informations['tweet_id'])
        sleep(0.5)
        
        narubot.favorite(narubot.informations['tweet_id'])
        sleep(0.5)
        
        
        if freshing_update_status == 0:
            freshing_update_status = int((60 * 60 * 3) / 2.5)
            frases = functions.get_phrases()
            narubot.update_status(choice(frases))
            
        freshing_update_status -= 1    
        loop += 1
        
        sleep(1)
    print('NaruBot desligado por 12hrs!')
    sleep(43200)