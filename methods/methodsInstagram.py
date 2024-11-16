import requests
import config

access_token = config.INSTAGRAM_ACCESS_TOKEN

def get_my_id():
    # Get the connected Instagram account ID
    endpoint = f'https://graph.facebook.com/v21.0/me/accounts?access_token={access_token}'

    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            page_id = data['data'][0]['id']
            # Get Instagram Business Account ID
            insta_endpoint = f'https://graph.facebook.com/v16.0/{page_id}?fields=instagram_business_account&access_token={access_token}'
            insta_response = requests.get(insta_endpoint)
            insta_data = insta_response.json()
            instagram_user_id = insta_data['instagram_business_account']['id']
            print(f"Instagram User ID: {instagram_user_id}")
        else:
            print("No connected pages found.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def fetch_all_posts(instagram_user_id):
    posts = []
    endpoint = f'https://graph.facebook.com/v21.0/{instagram_user_id}/media'
    params = {
        'fields': 'id,caption,timestamp',
        'limit': 100,  # Maximum allowed by the API
        'access_token': access_token
    }

    while True:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            posts.extend(data['data'])

            # Check for pagination
            if 'paging' in data and 'next' in data['paging']:
                endpoint = data['paging']['next']
                params = {}
            else:
                break
        else:
            print(f"Error fetching posts: {response.status_code}")
            print(response.text)
            break

    return posts

def fetch_one_post(media_id):
    like_endpoint = f'https://graph.facebook.com/v21.0/{media_id}?fields=like_count,caption,timestamp&access_token={access_token}'

    like_response = requests.get(like_endpoint)
    if like_response.status_code == 200:
        like_data = like_response.json()
        print(f"Media ID: {like_data['id']}, Caption: {like_data.get('caption', '')}, Timestamp: {like_data.get('timestamp', '')}")
    else:
        print(f"Error: {like_response.status_code}")
        print(like_response.text)

def fetch_post_insights(inst_id):
    # https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights

    # Check type of media
    media_endpoint = f'https://graph.facebook.com/v17.0/{inst_id}'
    media_params = {
        'fields': 'media_type',
        'access_token': access_token
    }
    media_response = requests.get(media_endpoint, params=media_params)
    if media_response.status_code == 200:
        media_data = media_response.json()
        media_type = media_data.get('media_type')
    else:
        print(f"Error fetching media type for InstId {inst_id}: {media_response.status_code}")
        print(media_response.text)
        return None, None
    
    # Based on media type, define the metrics to request
    if media_type == 'VIDEO' or media_type == 'REEL':
        metrics = 'reach,likes,saved,shares'
    else:
        metrics = 'reach,likes,saved,shares,follows'

    params = {
        'metric': metrics,
        'access_token': access_token
    }
    insights_endpoint = f'https://graph.facebook.com/v21.0/{inst_id}/insights'    

    response = requests.get(insights_endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        insights = {}
        for metric in data['data']:
            name = metric['name']
            value = metric['values'][0]['value']
            insights[name] = value
        return insights
    else:
        print(f"Error fetching insights for InstId {inst_id}: {response.status_code}")
        print(response.text)
        return None
    
