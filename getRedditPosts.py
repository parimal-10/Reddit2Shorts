import praw, os, json, random # type: ignore
import getSubreddit, getConfig, getVideoScript, markdownToText
from dotenv import load_dotenv #type: ignore

load_dotenv()

def __init_reddit():
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        password=os.getenv('REDDIT_PASSWORD'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        username=os.getenv('REDDIT_USERNAME'),
        check_for_async=False
    )
    return reddit

def get_content():
    try:
        reddit = __init_reddit()
    except:
        print("Error creating a reddit instance")
        return None
    
    existingVideos = __get_existing_post_ids(getConfig.get_ids_storage_file())
    posts = []

    postCount = getConfig.get_initial_post_count()
    attempts = 10

    while(postCount > 0):
        subreddit = getSubreddit.get_random_subreddit()
        submissions = reddit.subreddit(subreddit).top(time_filter="day", limit=15)
        if(attempts < 0): 
            return None
        for submission in submissions:
            if(submission.id in existingVideos or submission.over_18 or (submission.upvote_ratio < 0.8) or (not submission.is_self) or (not submission.selftext) or (len(submission.selftext.split()) > 120)):
                continue
            posts.append(submission)
            postCount -= 1
        if(postCount < 0):
            break
        attempts -= 1
    
    if(len(posts) == 0):
        return None

    return __get_content_from_posts(posts)

def __get_content_from_posts(posts):
    submission = random.choice(posts)
    print("random submission selected")
    print(submission.id, submission.url)
    content = getVideoScript.VideoScript(submission.title, submission.selftext, submission.id, submission.url)

    failedAttempts = 0
    for commment in submission.comments:
        if(content.addScene(commment.id, markdownToText.markdown_to_text(commment.body))):
            failedAttempts += 1
        if(content.can_be_finished()):
            break
        if(failedAttempts > 10):
            return None

    return content

def save_post_ids(post_id, fileName):
    ids = __get_existing_post_ids(fileName)
    ids.append(post_id)
    with open(fileName, "w") as file:
        json.dump(ids, file)

def __get_existing_post_ids(fileName):
    if not os.path.exists(fileName) or os.stat(fileName).st_size == 0:
        return []
    
    try:
        with open(fileName, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []