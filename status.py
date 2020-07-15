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

time = 60 * 60 * 1
sleep(60)

while True:
    frases = get_phrases()
    api.update_status(choice(frases))
    print('Tweet filosofico feito!')
    sleep(time)