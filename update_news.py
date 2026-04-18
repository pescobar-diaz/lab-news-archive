import requests
import json

# CONFIGURATION
HANDLE = "mundaylab.bsky.social"
FILE_NAME = "news.json"

def fetch_posts():
    try:
        with open(FILE_NAME, 'r') as f:
            archive = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        archive = []

    existing_ids = {post['cid'] for post in archive}
    
    url = f"https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor={HANDLE}&limit=100"
    response = requests.get(url).json()
    feed = response.get('feed', [])

    new_count = 0
    for item in feed:
        post = item['post']
        if post['cid'] not in existing_ids:
            image_url = None
            if 'embed' in post and 'images' in post['embed']:
                image_url = post['embed']['images'][0]['fullsize']

            # SAVE FACETS (This is what handles the links!)
            facets = post['record'].get('facets', [])

            archive.append({
                'cid': post['cid'],
                'text': post['record'].get('text', ''),
                'facets': facets,
                'createdAt': post['record'].get('createdAt'),
                'image': image_url,
                'uri': post['uri']
            })
            new_count += 1

    archive.sort(key=lambda x: x['createdAt'], reverse=True)
    with open(FILE_NAME, 'w') as f:
        json.dump(archive, f, indent=2)
    
    print(f"Success! Added {new_count} new posts.")

if __name__ == "__main__":
    fetch_posts()
