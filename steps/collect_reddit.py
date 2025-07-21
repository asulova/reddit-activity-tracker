from typing import List, Dict
from zenml import step, pipeline

# -------------------------------
# STEP 1 — Collect upvoted posts
# -------------------------------
@step
def collect_upvoted_posts(
    client_id: str,
    client_secret: str,
    username: str,
    password: str,
    user_agent: str = "upvote-tracker"
) -> List[Dict]:
    """
    Collect upvoted posts for a Reddit user.
    """
    import praw
    import datetime

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

    upvoted = []
    for item in reddit.user.me().upvoted(limit=None):
        if isinstance(item, praw.models.Submission):
            upvoted.append({
                'id': item.id,
                'type': 'upvoted_post',
                'subreddit': item.subreddit.display_name,
                'title': item.title,
                'body': item.selftext if hasattr(item, 'selftext') else '',
                'author': str(item.author),
                'url': item.url,
                'published': datetime.datetime.fromtimestamp(item.created_utc).isoformat(),
                'score': item.score,
                'num_comments': item.num_comments
            })
    return upvoted


# -------------------------------
# STEP 2 — Collect submissions & comments
# -------------------------------
@step
def collect_user_activity(
    client_id: str,
    client_secret: str,
    username: str,
    password: str,
    user_agent: str = "activity-tracker"
) -> List[Dict]:
    """
    Collect user submissions and comments.
    """
    import praw
    import datetime

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

    me = reddit.user.me()
    activity = []

    # Submissions
    for submission in me.submissions.new(limit=None):
        activity.append({
            'id': submission.id,
            'type': 'submission',
            'subreddit': submission.subreddit.display_name,
            'title': submission.title,
            'body': submission.selftext if hasattr(submission, 'selftext') else '',
            'author': str(submission.author),
            'url': submission.url,
            'published': datetime.datetime.fromtimestamp(submission.created_utc).isoformat(),
            'score': submission.score,
            'num_comments': submission.num_comments
        })

    # Comments
    for comment in me.comments.new(limit=None):
        activity.append({
            'id': comment.id,
            'type': 'comment',
            'subreddit': comment.subreddit.display_name,
            'title': '',
            'body': comment.body,
            'author': str(comment.author),
            'url': f"https://reddit.com{comment.permalink}",
            'published': datetime.datetime.fromtimestamp(comment.created_utc).isoformat(),
            'score': comment.score,
            'num_comments': ''
        })

    return activity

# -------------------------------
# STEP 3 — Save all to CSV
# -------------------------------
@step
def save_to_csv(
    activity: List[Dict],
    upvoted: List[Dict],
    csv_path: str
) -> str:
    """
    Save the combined user activity and upvoted posts to a specified CSV file.
    """
    import pandas as pd

    combined = activity + upvoted
    df = pd.DataFrame(combined)
    df.to_csv(csv_path, index=False)
    print(f"Saved {len(combined)} items to {csv_path}")
    return csv_path
