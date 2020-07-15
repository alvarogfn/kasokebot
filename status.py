from functions import get_phrases
from main import narubot
from random import choice
from os import environ
from time import sleep

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACESS_KEY = environ['ACESS_KEY']
ACESS_SECRET = environ['ACESS_SECRET']

narubot = narubot(CONSUMER_KEY, CONSUMER_SECRET, ACESS_KEY, ACESS_SECRET)

time = 60 * 60 * 1

while True:
    frases = get_phrases()
    narubot.update_status(choice(frases))
    print('Tweet filosofico feito!')
    sleep(time)