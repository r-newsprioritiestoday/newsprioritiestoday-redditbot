import requests 
import praw
from tinydb import TinyDB, Query, where
from tinydb_serialization import Serializer, SerializationMiddleware
from datetime import datetime, timedelta

# setup serializer, database and reddit bot

class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')


serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

db = TinyDB('../newsprioritiestoday-data/db.json', storage=serialization)  
reddit = praw.Reddit('bot', user_agent='newsprioritytoday:test user agent')



# get data from database and generate text



# get data that was created less than an hour ago.
# ideally the scraper and the bot should run at different times to avoid any result overlapping
results = db.search(where('datetime') > (datetime.now() - timedelta(hours = 1)))
#results = db.search((where('datetime') > (datetime.now() - timedelta(hours = 4))) & (where('datetime') < (datetime.now() - timedelta(hours = 5))))
# create reddit post
newssummary = "Here are your daily Top 5 news from all over the world: \n\n"

for result in results:
    newssummary += "## " + result["country"] + "\n"

    for article in result["articles"][:5]:
        # get translation
        if result['code'] != 'en':
            payload = {'q': article["headline"], 'langpair': result['code'] + '|en', 'de': 'do-oe@outlook.com'}
            r = requests.get('https://api.mymemory.translated.net/get', params=payload)
            
            response = r.json()
            newssummary += "- " + response["responseData"]["translatedText"]
        else:
            newssummary += "- " + article["headline"]

        if article["text"] != "":

            if result['code'] != 'en':
                payload = {'q': article["text"], 'langpair': result['code'] + '|en', 'de': 'do-oe@outlook.com'}
                r = requests.get('https://api.mymemory.translated.net/get', params=payload)
                print(r.text)
                response = r.json()
                newssummary += " - " + response["responseData"]["translatedText"]
            else:
                newssummary += " - " + article["text"]

        newssummary += "\n"
    
    newssummary += "\n^(Source: " + result["source"] + " @ " + str(result["datetime"]) + " UTC+1)"
    newssummary += "\n\n"

newssummary += "Headlines were machine-translated using translated.com services. \n\n"
newssummary += "For more, visit /r/newspriorities today."
    


print(newssummary)
input("\n\nPress Enter to post on subreddit...")

# post the info on the subreddit
subreddit = reddit.subreddit('newsprioritiestoday')

now = datetime.now()
subreddit.submit(now.strftime("%Y-%m-%d") + " - Daily News Priorities", selftext = newssummary)
