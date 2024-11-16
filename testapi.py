import requests
import secret

my_id = '17841459012723489'

def GetMyId(token):
    # Get the connected Instagram account ID
    endpoint = f'https://graph.facebook.com/v21.0/me/accounts?access_token={token}'

    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            page_id = data['data'][0]['id']
            # Get Instagram Business Account ID
            insta_endpoint = f'https://graph.facebook.com/v16.0/{page_id}?fields=instagram_business_account&access_token={token}'
            insta_response = requests.get(insta_endpoint)
            insta_data = insta_response.json()
            instagram_user_id = insta_data['instagram_business_account']['id']
            print(f"Instagram User ID: {instagram_user_id}")
        else:
            print("No connected pages found.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
def GetMediaId(instagram_user_id, token):
    # Replace 'instagram_user_id' with the ID obtained earlier
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
    # Replace with your Media ID
    like_endpoint = f'https://graph.facebook.com/v21.0/{media_id}?fields=like_count&access_token={token}'

    like_response = requests.get(like_endpoint)
    if like_response.status_code == 200:
        like_data = like_response.json()
        print(f"Number of likes: {like_data.get('like_count', 'N/A')}")
    else:
        print(f"Error: {like_response.status_code}")
        print(like_response.text)


# GetMyId(access_token)
idList = GetMediaId(my_id, access_token)
print(idList)

for id in idList:
    GetPostLikes(id, access_token)