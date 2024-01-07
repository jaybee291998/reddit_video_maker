from dotenv import load_dotenv
import praw
import os
from .model.entry import Entry

from .model.script import Script

load_dotenv(".env")

CLIENT_ID = os.getenv("CLIENT_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("PRAW_USERNAME")
USER_AGENT = os.getenv("USER_AGENT")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET_KEY,
    password=PASSWORD,
    user_agent=USER_AGENT,
    username=USERNAME
)

def get_scripts(sub_reddit_name: str, limit=5) -> list[Script]:
    subreddit = reddit.subreddit(sub_reddit_name)
    scripts: list[Script] = []
    for submission in subreddit.top(time_filter="day", limit=limit):
        script: Script = Script()
        script.url = submission.url
        script.folder_name = f"post-{submission.created_utc}-{submission.id}"
        script.submission = Entry(id=submission.id, title=submission.title, body=submission.selftext, file_name=f"post-{submission.id}", handle="")
        i = 0
        for comment in submission.comments:
            commentModel: Entry = Entry(title="", id=comment.id, body=comment.body, file_name=f"comment-{comment.id}", handle="")
            script.addComment(commentModel)
            i+=1
            if i > 5:
                break
        scripts.append(script)
    return scripts

# sc: Script = get_script(sub_reddit_name="AskReddit", limit=1)
# print(sc)
# print(sc.submission)
# print(sc.comments)
# print(sc.url)