import praw

reddit = praw.Reddit(
    client_id="cjSqmZBu90xGZJ4waJwo-A",
    client_secret="r07dF5EsaxdeY3Uv11LnffqKHZrYQg",
    password="Tomcaneat330tomatoes@291998",
    user_agent="1.0 by Pensive_Crab",
    username="pensive-crab",
)

subreddit = reddit.subreddit("ProgrammerHumor")

for submission in subreddit.top(limit=5):
    print(f"Title: {submission.title}")
    print(f"score: {submission.score}")
    print(f"URL: {submission.url}")
    print("\n")