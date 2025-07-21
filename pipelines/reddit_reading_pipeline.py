from zenml import pipeline
from steps.collect_reddit import collect_user_activity, collect_upvoted_posts, save_to_csv
from steps.visualize_reddit_reading import visualize_reading_history

CSV_PATH = 'reddit_activity.csv'

@pipeline(enable_cache=False)
def reddit_activity_pipeline(
    client_id: str,
    client_secret: str,
    username: str,
    password: str
):
    activity = collect_user_activity(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password
    )
    upvoted = collect_upvoted_posts(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password
    )
    csv_path  = save_to_csv(activity, upvoted, CSV_PATH)
    visualize_reading_history(csv_path)