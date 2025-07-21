import argparse
from pipelines.reddit_reading_pipeline import reddit_activity_pipeline
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Track Reddit upvoted posts/comments.")
    parser.add_argument(
        "--client-id", type=str, default=None, help="Reddit API client_id (for 'upvotes' pipeline)")
    parser.add_argument("--client-secret", type=str, default=None, help="Reddit API client_secret (for 'upvotes' pipeline)")
    parser.add_argument("--username", type=str, default=None, help="Reddit username (for 'upvotes' pipeline)")
    parser.add_argument("--password", type=str, default=None, help="Reddit password (for 'upvotes' pipeline)")
    args = parser.parse_args()

    client_id = args.client_id or os.getenv("REDDIT_CLIENT_ID") or input("Reddit client_id: ")
    client_secret = args.client_secret or os.getenv("REDDIT_CLIENT_SECRET") or input("Reddit client_secret: ")
    username = args.username or os.getenv("REDDIT_USERNAME") or input("Reddit username: ")
    password = args.password or os.getenv("REDDIT_PASSWORD") or input("Reddit password: ")
   
    reddit_activity_pipeline(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password
    )

if __name__ == "__main__":
    main()
