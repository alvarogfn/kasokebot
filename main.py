import tweepy
from os import environ
from boto.s3.connection import S3Connection
from time import sleep
from datetime import datetime
import json

def save(database, user):
    
    ext = f'database\\database{datetime.now().year}.json' 
    try:
        open(ext, 'r').close()
    except FileNotFoundError:
        open(ext, 'x').close()
        data = {}
        data['total'] = 0
            
        with open(ext, 'w') as outfile:
            json.dump(data, outfile, indent=4)
        outfile.close()
        sleep(0.1)
    finally:
        with open(ext, 'r+') as outfile:
            dataupdate = json.load(outfile)     
            
            if user in dataupdate.keys():
                database['TOTAL_USES'] += dataupdate[user]['TOTAL_USES']
                
            data = {}
            data[user] = database
            
            dataupdate['total'] += 1
            dataupdate.update(data)
            outfile.seek(0)
            json.dump(dataupdate, outfile, indent=4)
            outfile.close()

def reply_status(screen_name, tweetid):
    api.retweet(tweetid)
    api.create_favorite(tweetid)
    api.update_with_media(status=f'@{screen_name} Bayo!', in_reply_to_status_id=tweetid, filename='dattebayo.gif')
        
class stalker(tweepy.StreamListener):
    def on_status(self, status):
        user = status.user.screen_name
        userid = status.user.id
        tweetid = status.id
        day = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}'
        time = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'
        
        database = {'USER_ID': userid, 
                    'TOTAL_USES': 1, 
                    'LAST_OPERATION_TIME': [day, time]}
        sleep(0.5)
        save(database, user)
        sleep(1.5)
        reply_status(user, tweetid)
        sleep(1.5)
    
    def on_error(self, status_error):
        if status_error == 420:
            return False
    
CONSUMER_KEY = S3Connection(environ['CONSUMER_KEY'])
CONSUMER_SECRET = S3Connection(environ['CONSUMER_SECRET'])
ACCESS_KEY = S3Connection(environ['ACESS_KEY'])
ACCESS_SECRET = S3Connection(environ['ACESS_SECRET'])

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

api.update_status('Datebayo: On! :)')
stalker = stalker()
stalking = tweepy.Stream(auth=api.auth, listener=stalker)
stalking.filter(track=['Dattebayo!'])
api.update_status('Datebayo: Off! :(')