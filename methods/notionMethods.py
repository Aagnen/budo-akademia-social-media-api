import requests
import config
from notion_client import Client
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

notion = Client(auth=config.NOTION_API_TOKEN)


def create_notion_page(inst_id, caption, timestamp, database_id):
    """
    Create a new page in the Notion database with the given Instagram data.

    Args:
        inst_id (str): The Instagram ID.
        caption (str): The caption of the Instagram post.
        timestamp (str): The timestamp of the post.
        database_id (str): The Notion database ID.

    Returns:
        dict or None: The response from Notion API if successful, None otherwise.
    """
    properties = {
        "InstId": {
            "rich_text": [{
                "type": "text",
                "text": {"content": inst_id}
            }]
        },
        "caption": {
            "rich_text": [{
                "type": "text",
                "text": {"content": caption or ""}
            }]
        },
        "Wstawiony": {
            "date": {
                "start": timestamp  # Using the timestamp from Instagram
            }
        }
    }

    try:
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
        logger.info(f"Created page for InstId: {inst_id}")
        return response
    except Exception as e:
        logger.error(f"Error creating page for InstId {inst_id}: {e}")
        return None


def page_exists(inst_id, database_id):
    """
    Check if a page with the given InstId exists in the Notion database.

    Args:
        inst_id (str): The Instagram ID.
        database_id (str): The Notion database ID.

    Returns:
        bool: True if the page exists, False otherwise.
    """
    try:
        response = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "InstId",
                "rich_text": {
                    "equals": inst_id
                }
            }
        )
        exists = len(response['results']) > 0
        logger.debug(f"Page exists for InstId {inst_id}: {exists}")
        return exists
    except Exception as e:
        logger.error(f"Error checking if page exists for InstId {inst_id}: {e}")
        return False


def get_notion_entries_with_property(database_id, property_name):
    """
    Retrieve entries from the Notion database where the specified property is not empty.

    Args:
        database_id (str): The Notion database ID.
        property_name (str): The property to filter on.

    Returns:
        list: A list of Notion page entries.
    """
    entries = []
    try:
        has_more = True
        next_cursor = None
        while has_more:
            params = {
                "database_id": database_id,
                "filter": {
                    "property": property_name,
                    "rich_text": {"is_not_empty": True}
                }
            }
            if next_cursor:
                params['start_cursor'] = next_cursor

            response = notion.databases.query(**params)
            entries.extend(response['results'])
            has_more = response.get('has_more', False)
            next_cursor = response.get('next_cursor')
    except Exception as e:
        logger.error(f"Error fetching Notion entries: {e}")
    return entries  # Ensure entries are returned regardless of exceptions


def update_notion_entry_with_insights(page_id, insights, platform):
    """
    Update a Notion page with insights data from a specified platform.

    Args:
        page_id (str): The Notion page ID.
        insights (dict): A dictionary containing insights data.
        platform (str): The platform name ('Instagram' or 'TikTok').

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    properties = {}
    if platform.lower() == 'instagram':
        properties.update({
            'Inst reach': {'number': insights.get('reach', 0)},
            'Inst likes': {'number': insights.get('likes', 0)},
            'Inst saves': {'number': insights.get('saved', 0)},
            'Inst Shares': {'number': insights.get('shares', 0)},
            'Inst FollowUps': {'number': insights.get('follows')}
            if 'follows' in insights else {'number': None}
        })
    elif platform.lower() == 'tiktok':
        properties.update({
            'Tiktok reach': {'number': insights.get('Plays', 0)},  # Plays correspond to reach
            'Tiktok likes': {'number': insights.get('Likes', 0)},
            'Tiktok shares': {'number': insights.get('Shares', 0)}
        })
    else:
        logger.error(f"Unsupported platform: {platform}")
        return False

    try:
        notion.pages.update(page_id=page_id, properties=properties)
        logger.info(f"Updated Notion page {page_id} with {platform} insights.")
        return True
    except Exception as e:
        logger.error(f"Error updating Notion page {page_id}: {e}")
        return False
