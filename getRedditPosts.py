import praw # type: ignore
import os
from dotenv import load_dotenv #type: ignore
from getSubreddit import *
from getConfig import *

load_dotenv()

def initReddit():
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        password=os.getenv('REDDIT_PASSWORD'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        username=os.getenv('REDDIT_USERNAME'),
        check_for_async=False
    )
    return reddit

def getContent(outputDir):
    reddit = initReddit()
    subreddit = getRandomSubreddit()
    submissions = reddit.subreddit(subreddit).top("day", limit=3)
    existingVideos = getExistingPostIds(outputDir)
    posts = []
    for submission in submissions:
        if(submission.id in existingVideos or submission.over_18):
            continue
        posts.append(submission)
    return posts


def getExistingPostIds(outputDir):
    files = os.listdir(outputDir + "/videos")
    return [os.path.splitext(file)[0] for file in files]