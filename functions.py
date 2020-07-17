def no_text(text):
    return lambda filter: text.split()[0] != filter
    
def tweets_track():
    import json
    with open('database.json', 'r+') as outfile:
        database = json.load(outfile)
        data = {}
        data['tweets_track'] = database['tweets_track']
        data['tweets_track'] += 1
        database.update(data)
        outfile.seek(0)
        json.dump(database, outfile, indent=4)
        outfile.close()
        return data['tweets_track']

def time_for_sleep():
    from datetime import datetime
    time = datetime.now().hour * 60 * 60
    time += datetime.now().minute * 60
    time += datetime.now().second
    time = 86400 - time
    return time

