import tweepy
from os import environ
from time import sleep
from functions import *
from datetime import datetime

class kasokebot(tweepy.StreamListener):
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACESS_KEY, ACESS_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
         
    def streaming(self, track):
        stalking = tweepy.Stream(auth=self.api.auth, listener=self)
        stalking.filter(track=track, languages=['pt', 'en'])
    
    def on_status(self, status):
        self.user_id = None
        if not retweet_check(status):
            if not self.user_id == status.user.id:
                try:
                    self.tweet_text = status.extended_tweet["full_text"]
                except AttributeError:
                    self.tweet_text = status.text
                finally:
                    self.tweet_id = status.id
                    self.user_id = status.user.id
                    print('Tweet tracked!')
                    return False
        
    def retweet(self):
        try:
            self.api.retweet(self.tweet_id)
        except tweepy.RateLimitError:
            print('    Retweet limit exceeded.')
        except Exception as error:
            print('    Retweet failed.', error)
        else:         
            print('    Retweet done.')
 
    
    def favorite(self):
        try: 
            self.api.create_favorite(self.tweet_id)
        except tweepy.RateLimitError:
            print('    Favorite limit exceeded.')
        except Exception as error:
            print('    Favorite failed. ', error)   
        else:         
            print('    Favorite done.')
    
    def report(self):
        try:
            self.api.report_spam(self.tweet_id)
        except:
            print('        Spam reported failed.')
        else:
            print('        Spam reported.')
            
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

tracker = ['dattebayo', 'dattebayo!']

filtro = ['auge', 'maconha', 'bolsonaro', 'sorriso', 'macaco' 'otário', 'tem bot pra tudo', 'vassoura', 'old', 'que', 'joão pessoa', 'recife', 'noia', 'cachorra' 'quarentena', 'computador', 'teclado', 'frango', 'cu', 'grilo', 'nóia', 'corno', 'hatsune', 'dahyun', 'nayeon', 'jeongyeon', 'javascript', 'mano', 'busão', 'fada sensata', 'puta', 'enzo', 'gripezinha', 'desemprego', 'assistir', 'minsung', 'desculpa por ser homem', 'caraio', 'maicon kuster', 'bot', 'farofa', '#MTVHottest', 'Ariana Grande']
 
while True:
    try:
        narubot.streaming(tracker)
        if not spam_test(narubot.tweet_text, filtro):
            if len_test(narubot.tweet_text):
                narubot.retweet()
                narubot.favorite()
            else:
                print('    Tweet too small.')         
        else:
            print('    Spam detected.')
            narubot.report()
        sleep(5)
    except Exception as error:
        print(f'Last error: {error}')
        
