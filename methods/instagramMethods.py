import requests
import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ACCESS_TOKEN = config.INSTAGRAM_ACCESS_TOKEN
API_VERSION = 'v17.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}/'


def get_instagram_user_id():
    """
    Retrieve the Instagram Business Account ID connected to your Facebook account.

    Returns:
        str: The Instagram User ID if found, None otherwise.
    """
    endpoint = f'{BASE_URL}me/accounts'
    params = {
        'access_token': ACCESS_TOKEN
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('data'):
            page_id = data['data'][0]['id']
            # Get Instagram Business Account ID
            insta_endpoint = f'{BASE_URL}{page_id}'
            insta_params = {
                'fields': 'instagram_business_account',
                'access_token': ACCESS_TOKEN
            }
            insta_response = requests.get(insta_endpoint, params=insta_params)
            insta_response.raise_for_status()
            insta_data = insta_response.json()
            instagram_user_id = insta_data.get('instagram_business_account', {}).get('id')
            if instagram_user_id:
                logger.info(f"Instagram User ID: {instagram_user_id}")
                return instagram_user_id
            else:
                logger.warning("No Instagram Business Account connected to the page.")
                return None
        else:
            logger.warning("No connected pages found.")
            return None
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while getting Instagram User ID: {http_err}")
        logger.debug(response.text)
    except Exception as err:
        logger.error(f"An error occurred while getting Instagram User ID: {err}")
    return None


def fetch_all_posts(instagram_user_id):
    """
    Fetch all media posts from the Instagram account.

    Args:
        instagram_user_id (str): The Instagram User ID.

    Returns:
        list: A list of posts with 'id', 'caption', and 'timestamp'.
    """
    posts = []
    endpoint = f'{BASE_URL}{instagram_user_id}/media'
    params = {
        'fields': 'id,caption,timestamp',
        'limit': 100,  # Maximum allowed by the API
        'access_token': ACCESS_TOKEN
    }

    try:
        while True:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            posts.extend(data.get('data', []))

            # Check for pagination
            paging = data.get('paging', {})
            next_page = paging.get('next')
            if next_page:
                endpoint = next_page
                params = {}
            else:
                break
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while fetching posts: {http_err}")
        logger.debug(response.text)
    except Exception as err:
        logger.error(f"An error occurred while fetching posts: {err}")

    return posts


def fetch_post_details(media_id):
    """
    Fetch details of a single Instagram media post.

    Args:
        media_id (str): The Media ID of the post.

    Returns:
        dict: A dictionary containing media details like 'id', 'caption', and 'timestamp'.
    """
    endpoint = f'{BASE_URL}{media_id}'
    params = {
        'fields': 'id,caption,timestamp',
        'access_token': ACCESS_TOKEN
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        media_data = response.json()
        logger.info(f"Fetched details for Media ID: {media_data.get('id')}")
        return media_data
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while fetching media details: {http_err}")
        logger.debug(response.text)
    except Exception as err:
        logger.error(f"An error occurred while fetching media details: {err}")
    return None


def fetch_post_insights(media_id):
    """
    Fetch insights for a specific Instagram media post.
    See official documentation: https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights

    Args:
        media_id (str): The Media ID of the Instagram post.

    Returns:
        dict: A dictionary containing insights metrics.
    """
    try:
        # Check the type of media
        media_endpoint = f'{BASE_URL}{media_id}'
        media_params = {
            'fields': 'media_type',
            'access_token': ACCESS_TOKEN
        }
        media_response = requests.get(media_endpoint, params=media_params)
        media_response.raise_for_status()
        media_data = media_response.json()
        media_type = media_data.get('media_type')

        if not media_type:
            logger.error(f"Media type not found for Media ID {media_id}")
            return None

        # Based on media type, define the metrics to request
        if media_type in ['VIDEO', 'REEL']:
            metrics = 'reach,likes,saved,shares'
        else:
            metrics = 'reach,likes,saved,shares,follows'

        insights_endpoint = f'{BASE_URL}{media_id}/insights'
        insights_params = {
            'metric': metrics,
            'access_token': ACCESS_TOKEN
        }

        response = requests.get(insights_endpoint, params=insights_params)
        response.raise_for_status()
        data = response.json()
        insights = {}
        for metric in data.get('data', []):
            name = metric.get('name')
            values = metric.get('values', [])
            if values:
                value = values[0].get('value')
                insights[name] = value
        logger.info(f"Fetched insights for Media ID {media_id}")
        return insights
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while fetching insights for Media ID {media_id}: {http_err}")
        logger.debug(response.text)
    except Exception as err:
        logger.error(f"An error occurred while fetching insights for Media ID {media_id}: {err}")
    return None
