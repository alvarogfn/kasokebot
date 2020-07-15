from functions import get_phrases
import tweepy
from random import choice
from os import environ
from time import sleep

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACESS_KEY = environ['ACESS_KEY']
ACESS_SECRET = environ['ACESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACESS_KEY, ACESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

sleep(60)
time = 60 * 60 * 2
contador = 1

while True:
    frases = get_phrases()
    try:
        api.update_status(choice(frases))
        
    except tweepy.RateLimitError:
        print('Limite de tweets diarios atingido.')
        
    except tweepy.TweepError: 
        print('Falha ao enviar tweet.')
    else:
        print(f'{contador}º Tweet feito!')
        contador += 1
    
    sleep(time)
