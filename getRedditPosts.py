import praw, os, json # type: ignore
from getSubreddit import *
from getConfig import *
from dotenv import load_dotenv #type: ignore

load_dotenv()

def init_reddit():
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        password=os.getenv('REDDIT_PASSWORD'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        username=os.getenv('REDDIT_USERNAME'),
        check_for_async=False
    )
    return reddit

def get_content(outputDir):
    reddit = init_reddit()
    subreddit = get_random_subreddit()
    submissions = reddit.subreddit(subreddit).top(time_filter="day", limit=15)
    existingVideos = get_existing_post_ids(get_ids_storage_file())
    posts = []
    for submission in submissions:
        if(submission.id in existingVideos or submission.over_18 or submission.upvote_ratio < 0.9 or (not submission.is_self) or (not submission.selftext) or submission.selftext.split() > 100):
            continue
        posts.append(submission)
        print(vars(submission))
    return get_content_from_posts(posts)

def get_content_from_posts(posts):
    # title, selftext
    return 1


def save_post_ids(post_ids, filename):
    existing_ids = get_existing_post_ids(filename)
    updated_ids = list(set(existing_ids + post_ids))
    with open(filename, "w") as file:
        json.dump(updated_ids, file)

# Load postIds from a file
def get_existing_post_ids(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []