import requests
import mySecret

# Gets last 25 posts
def GetMediaId(instagram_user_id, token):
    media_endpoint = f'https://graph.facebook.com/v21.0/{instagram_user_id}/media?fields=id&access_token={token}'

    idList = []
    media_response = requests.get(media_endpoint)
    if media_response.status_code == 200:
        media_data = media_response.json()
        for media in media_data['data']:
            # print(media)
            idList.append(media['id'])
            # print(f"Media ID: {media['id']}, Likes: {media.get('like_count', '')}")
    else:
        print(f"Error: {media_response.status_code}")
        print(media_response.text)
    return idList
def GetPostLikes(media_id, token):
    like_endpoint = f'https://graph.facebook.com/v21.0/{media_id}?fields=like_count&access_token={token}'

    like_response = requests.get(like_endpoint)
    if like_response.status_code == 200:
        like_data = like_response.json()
        print(f"Number of likes: {like_data.get('like_count', 'N/A')}")
    else:
        print(f"Error: {like_response.status_code}")
        print(like_response.text)
def GetPostData(media_id, token):
    insights_endpoint = f'https://graph.facebook.com/v21.0/{media_id}/insights'
    metrics = 'likes,comments,reach,saved,shares,follows'
    params = {
        'metric': metrics,
        'access_token': token
    }
    
    insights_response = requests.get(insights_endpoint, params=params)
    
    if insights_response.status_code == 200:
        insights_data = insights_response.json()
        print(f"POST: {media_id}")
        for metric in insights_data['data']:
            name = metric['name']
            value = metric['values'][0]['value']
            print(f"{name.capitalize()}: {value}")
    else:
        print(f"Error: {insights_response.status_code}")
        print(insights_response.text)

idList = GetMediaId(mySecret.my_id, mySecret.access_token)

for id in idList:
    # GetPostLikes(id, mySecret.access_token)
    GetPostData(id, mySecret.access_token)