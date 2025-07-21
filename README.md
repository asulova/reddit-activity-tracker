# Reddit Activity Tracker Pipeline

Track and visualize your Reddit upvoted posts, submissions, and comments using a modular analytics pipeline built with [ZenML](https://github.com/zenml-io/zenml).

## Overview

This project demonstrates how to build a personal analytics pipeline to collect and analyze your Reddit activity. It leverages ZenML for pipeline orchestration and PRAW for Reddit API access.

## Architecture

ZenML is an MLOps framework that lets you define:

- **Steps**: Modular, reusable functions that produce or consume artifacts.
- **Pipelines**: Ordered sequences of steps wired together.
- **Stacks**: Execution environments, artifact stores, orchestrators, etc.

### Pipeline Steps

The pipeline consists of four main steps:

1. **`collect_user_activity`**: Collects your Reddit submissions and comments.
2. **`collect_upvoted_posts`**: Collects posts you have upvoted on Reddit.
3. **`save_to_csv`**: Saves all collected activity and upvoted posts to a CSV file.
4. **`visualize_reddit_reading`**: Visualizes your Reddit activity (e.g., top subreddits, activity per month).

These steps are combined in a single ZenML pipeline:

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
│   └── reddit_reading_pipeline.py   # Pipeline definition
├── run.py                          # CLI entrypoint
├── steps/
│   ├── collect_reddit.py           # Reddit data collection steps
│   └── visualize_reddit_reading.py # Visualization step
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd reddit-activity-tracker
python -m venv venv
# On Unix/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Initialize ZenML

```bash
zenml init
```

### 3. Configure Reddit API Credentials

- Create a Reddit app at [Reddit Apps](https://www.reddit.com/prefs/apps)
- Set the following environment variables **or** pass them as CLI arguments:
  - `REDDIT_CLIENT_ID`
  - `REDDIT_CLIENT_SECRET`
  - `REDDIT_USERNAME`
  - `REDDIT_PASSWORD`

### 4. Run the Pipeline

```bash
python run.py --client-id <id> --client-secret <secret> --username <user> --password <pass>
```
Or, if environment variables are set:
```bash
python run.py
```

## Output

- A CSV file (`reddit_activity.csv`) containing all your Reddit activity and upvoted posts.
- A visualization window showing your top subreddits and activity per month.

## How It Works

- **Reddit Data Collection**: Uses PRAW to fetch your submissions, comments, and upvoted posts.
- **CSV Export**: Combines all activity into a single CSV file.
- **Visualization**: Plots your most active subreddits and activity over time.

---

Powered by [ZenML](https://zenml.io/).
