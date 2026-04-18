import requests
import json
import os

# CONFIGURATION
HANDLE = "pescobar-diaz.bsky.social" # Update this to your lab's handle
FILE_NAME = "news.json"

def fetch_posts():
    # 1. Load existing archive
    try:
        with open(FILE_NAME, 'r') as f:
            archive = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        archive = []

    existing_ids = {post['cid'] for post in archive}
    
    # 2. Get latest posts from Bluesky
    url = f"https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor={HANDLE}&limit=100"
    response = requests.get(url).json()
    feed = response.get('feed', [])

    # 3. Add new ones
    new_count = 0
    for item in feed:
        post = item['post']
        if post['cid'] not in existing_ids:
            # Check for images
            image_url = None
            if 'embed' in post and 'images' in post['embed']:
                image_url = post['embed']['images'][0]['fullsize']

            archive.append({
                'cid': post['cid'],
                'text': post['record'].get('text', ''),
                'createdAt': post['record'].get('createdAt'),
                'image': image_url,
                'uri': post['uri']
            })
            new_count += 1

    # 4. Sort (Newest first) and Save
    archive.sort(key=lambda x: x['createdAt'], reverse=True)
    with open(FILE_NAME, 'w') as f:
        json.dump(archive, f, indent=2)
    
    print(f"Success! Added {new_count} new posts.")

if __name__ == "__main__":
    fetch_posts()
