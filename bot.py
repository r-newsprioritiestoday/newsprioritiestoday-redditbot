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

db = TinyDB('../data/db.json', storage=serialization)  
reddit = praw.Reddit('bot', user_agent='newsprioritytoday:test user agent')



# get data from database and generate text



# get data that was created less than an hour ago.
# ideally the scraper and the bot should run at different times to avoid any result overlapping
results = db.search(where('datetime') > (datetime.now() - timedelta(hours = 1)))

# create reddit post
newssummary = "Here are your daily Top 5 news from all over the world: \n\n"
newssummary += "All news are kept in their original language. To translate to english, right click on a sentence an select 'Translate to english' (in chrome) \n\n"

for result in results:
    newssummary += "## " + result["country"] + "\n"

    for article in result["articles"][:5]:
        newssummary += "- " + article["headline"]
        if article["text"] != "":
            newssummary += " - " + article["text"]

        newssummary += "\n"
    
    newssummary += "\n^(Source: " + result["source"] + " @ " + str(result["datetime"]) + ")"
    newssummary += "\n\n"

newssummary += "For more, visit /r/newspriorities today."
    


print(newssummary)
# post the info on the subreddit
subreddit = reddit.subreddit('reddit_api_test')

now = datetime.now()
# subreddit.submit(now.strftime("%Y-%m-%d") + " - Daily News Priorities", selftext = newssummary)