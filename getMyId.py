import requests
import secret


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

GetMyId(secret.access_token)