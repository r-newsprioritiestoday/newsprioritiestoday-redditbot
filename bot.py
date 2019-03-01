import praw

reddit = praw.Reddit('bot', user_agent='newsprioritytoday:test user agent')

subreddit = reddit.subreddit('newsprioritiestoday')

print(subreddit.display_name)
print(subreddit.title)
print(subreddit.description)