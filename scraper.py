import feedparser
import json

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

    # Prepare the data for JSON (only title and link)
    json_data = []
    for entry in all_entries:
        json_data.append({
            'title': entry.title,
            'link': entry.link
        })

    # Save the data to a JSON file
    with open('mental_health_links.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    # Optionally print the JSON data to the terminal
    for entry in json_data:
        print(f"Title: {entry['title']}")
        print(f"Link: {entry['link']}")
        print("-" * 80)

if __name__ == "__main__":
    main()
