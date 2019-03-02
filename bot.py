import praw
from tinydb import TinyDB, Query, where
from tinydb_serialization import Serializer, SerializationMiddleware
from datetime import datetime

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


print(db.search(where('datetime') < datetime.now()))

newssummary

# get data from database and generate text



# post the info on the subreddit
subreddit = reddit.subreddit('reddit_api_test')

now = datetime.now()
# subreddit.submit(now.strftime("%Y-%m-%d") + " - Daily News Priorities", selftext = newssummary)