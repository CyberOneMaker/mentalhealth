import feedparser
import json
import os
from git import Repo

# List of RSS feed URLs
rss_feeds = [
    'https://www.nami.org/Blogs/NAMI-Blog?rss=1',
    'https://www.mentalhealthamerica.net/rss.xml',
    'https://www.psychologytoday.com/us/rss.xml',
    'https://www.healthline.com/rss',
    'https://rss.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC'
]

# Keywords to filter articles
keywords = ['suicide', 'suicidal ideation', 'depression', 'mental health', 'anxiety']

def fetch_feed_entries(feed_url):
    feed = feedparser.parse(feed_url)
    return feed.entries

def filter_entries_by_keywords(entries, keywords):
    filtered_entries = []
    for entry in entries:
        if any(keyword.lower() in (entry.title + entry.summary).lower() for keyword in keywords):
            filtered_entries.append(entry)
    return filtered_entries

def main():
    all_entries = []
    for feed_url in rss_feeds:
        entries = fetch_feed_entries(feed_url)
        filtered_entries = filter_entries_by_keywords(entries, keywords)
        all_entries.extend(filtered_entries)

    # Prepare the data for JSON
    json_data = []
    for entry in all_entries:
        json_data.append({
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary
        })

    # Save the data to a JSON file
    with open('mental_health_links.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    # Push the JSON file to GitHub
    repo_path = '.'  # Path to your local repository
    repo = Repo(repo_path)
    repo.git.add('mental_health_links.json')
    repo.index.commit('Update mental health links')
    origin = repo.remote(name='origin')
    origin.push()

if __name__ == "__main__":
    main()
