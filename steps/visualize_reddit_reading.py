import pandas as pd
import matplotlib.pyplot as plt
import os
from zenml import step
from typing import List

@step
def write_articles_to_csv(articles: List[dict], csv_path: str) -> str:
    COLUMNS = ['title', 'author', 'published', 'url']
    if articles:
        df = pd.DataFrame(articles)
        if os.path.exists(csv_path):
            df_existing = pd.read_csv(csv_path)
            df = pd.concat([df_existing, df], ignore_index=True).drop_duplicates(subset=['url'])
        df.to_csv(csv_path, index=False)
        print(f"Saved {len(df)} articles to {csv_path}")
    else:
        print("No new articles found.")
        if not os.path.exists(csv_path):
            pd.DataFrame(columns=COLUMNS).to_csv(csv_path, index=False)
    return csv_path

@step
def visualize_reading_history(csv_path: str) -> None:
    if not os.path.exists(csv_path):
        print(f"File {csv_path} does not exist. Nothing to visualize.")
        return
    df = pd.read_csv(csv_path)
    if df.empty:
        print("No data to visualize.")
        return

    # Most-read authors
    author_counts = df['author'].value_counts().head(10)
    print("Most-read authors:")
    print(author_counts)
    author_counts.plot(kind='bar', title='Top 10 Most-Read Authors')
    plt.ylabel('Articles Read')
    plt.tight_layout()
    plt.show()

    # Articles per month
    if 'published' in df.columns:
        df['published'] = pd.to_datetime(df['published'], errors='coerce')
        df['month'] = df['published'].dt.to_period('M')
        month_counts = df['month'].value_counts().sort_index()
        print("Articles read per month:")
        print(month_counts)
        month_counts.plot(kind='bar', title='Articles Read Per Month')
        plt.ylabel('Articles Read')
        plt.tight_layout()
        plt.show() 