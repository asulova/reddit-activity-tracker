# Reddit Upvote Tracker Pipeline

This repository demonstrates how to build a personal analytics pipeline with [ZenML](https://github.com/zenml-io/zenml) to track and visualize your Reddit upvoted posts, submissions, and comments.

## Concept & Architecture

ZenML is an MLOps framework that lets you define:

1. **Steps**: Modular, reusable functions that produce/consume artifacts.
2. **Pipelines**: Ordered sequences of steps wired together.
3. **Stacks**: Execution environments, artifact stores, orchestrators, etc.

Here, our pipeline has four steps:

- **`collect_user_activity`**
  - Collects your Reddit submissions and comments.
- **`collect_upvoted_posts`**
  - Collects posts you have upvoted on Reddit.
- **`save_to_csv`**
  - Saves all collected activity and upvoted posts to a CSV file.
- **`visualize_reddit_reading`**
  - Visualizes your Reddit activity (top subreddits, activity per month, etc.).

These steps are wired into a single ZenML pipeline:

```python
@pipeline
def reddit_activity_pipeline(client_id, client_secret, username, password):
    activity = collect_user_activity(client_id, client_secret, username, password)
    upvoted = collect_upvoted_posts(client_id, client_secret, username, password)
    csv_path = save_to_csv(activity, upvoted)
    visualize_reddit_reading(csv_path)
```

## Repository Structure

```
.
├── pipelines/
│   └── reddit_reading_pipeline.py   ← pipeline definition
├── run.py                          ← CLI entrypoint
├── steps/
│   ├── collect_reddit.py           ← Reddit data collection steps
│   └── visualize_reddit_reading.py ← Visualization step
├── requirements.txt
└── README.md
```

## Getting Started

1. **Clone & Install**

```bash
git clone <your-repo-url>
cd reddit-upvote-tracker
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. **Initialize ZenML**
```bash
zenml init
```

3. **Configure Reddit API Credentials**
- Create a Reddit app at https://www.reddit.com/prefs/apps
- Set environment variables or pass as CLI args:
  - `REDDIT_CLIENT_ID`
  - `REDDIT_CLIENT_SECRET`
  - `REDDIT_USERNAME`
  - `REDDIT_PASSWORD`

4. **Run the Pipeline**

```bash
python run.py --client-id <id> --client-secret <secret> --username <user> --password <pass>
```
Or set the environment variables and just run:
```bash
python run.py
```

## Output
- A CSV file (`reddit_activity.csv`) with all your Reddit activity and upvoted posts.
- A visualization window showing your top subreddits and activity per month.

## What’s Happening Under the Hood?

1. **Reddit Data Collection**
   - Uses PRAW to fetch your submissions, comments, and upvoted posts.
2. **CSV Export**
   - Combines all activity into a single CSV file.
3. **Visualization**
   - Plots your most active subreddits and activity over time.

---

Powered by ZenML.
