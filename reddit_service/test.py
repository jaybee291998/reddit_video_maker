from dotenv import load_dotenv
import praw
import os
from .model.entry import Entry
import configparser

from .model.script import Script

load_dotenv(".env")

config = configparser.ConfigParser()
config.read("settings.ini")
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

MAX_CHAR_COUNT = int(config["RedditService"]["comment_max_char_count"])
MAX_COMMENT_COUNT = int(config["RedditService"]["max_number_of_comment"])

def get_scripts(sub_reddit_name: str, limit=5) -> list[Script]:
    subreddit = reddit.subreddit(sub_reddit_name)
    scripts: list[Script] = []
    for submission in subreddit.top(time_filter="day", limit=limit):
        if submission.over_18:
            continue
        script: Script = Script()
        script.url = submission.url
        script.folder_name = f"post-{submission.created_utc}-{submission.id}"
        script.submission = Entry(id=submission.id, title=submission.title, body=submission.selftext, file_name=f"post-{submission.id}", handle="")
        i = 0
        for comment in submission.comments:
            if len(comment.body) > MAX_CHAR_COUNT:
                continue
            commentModel: Entry = Entry(title="", id=comment.id, body=comment.body, file_name=f"comment-{comment.id}", handle="")
            script.addComment(commentModel)
            i+=1
            if i > MAX_COMMENT_COUNT:
                break
        scripts.append(script)
    return scripts

# sc: Script = get_script(sub_reddit_name="AskReddit", limit=1)
# print(sc)
# print(sc.submission)
# print(sc.comments)
# print(sc.url)