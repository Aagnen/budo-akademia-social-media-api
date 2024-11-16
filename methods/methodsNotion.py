import requests
import config
from notion_client import Client

notion = Client(auth=config.NOTION_API_TOKEN)

def create_notion_page(inst_id, caption, timestamp, database_id):
    try:
        response = notion.pages.create(
            **{
                "parent": {"database_id": database_id},
                "properties": {
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
            }
        )
        print(f"   Created page for InstId: {inst_id}")
    except Exception as e:
        print(f"   Error creating page for InstId {inst_id}: {e}")

def if_page_exists(inst_id, database_id):
    try:
        # Query the database to check for pages with the given InstId
        response = notion.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "property": "InstId",
                    "rich_text": {
                        "equals": inst_id
                    }
                }
            }
        )
        return len(response['results']) > 0
    except Exception as e:
        print(f"Error checking if page exists for InstId {inst_id}: {e}")
        return False
    
def get_notion_entries_with_instid(database_id):
    entries = []
    try:
        has_more = True
        next_cursor = None
        while has_more:
            params = {
                "database_id": database_id,
                "filter": {
                    "property": "InstId",
                    "rich_text": {"is_not_empty": True}
                }
            }
            if next_cursor:
                params['start_cursor'] = next_cursor

            response = notion.databases.query(**params)
            entries.extend(response['results'])
            has_more = response['has_more']
            next_cursor = response.get('next_cursor')
    except Exception as e:
        print(f"Error fetching Notion entries: {e}")
    return entries

def update_notion_entry_with_insights(page_id, insights):
    properties = {}
    properties['Inst reach'] = {'number': insights.get('reach', 0)}
    properties['Inst likes'] = {'number': insights.get('likes', 0)}
    properties['Inst saves'] = {'number': insights.get('saved', 0)}
    properties['Inst Shares'] = {'number': insights.get('shares', 0)}

    if 'follows' in insights:
        properties['Inst FollowUps'] = {'number': insights.get('follows', 0)}
    else:
        properties['Inst FollowUps'] = {'number': None}

    try:
        notion.pages.update(page_id=page_id, properties=properties)
        print(f"Updated Notion page {page_id} with insights.")
    except Exception as e:
        print(f"Error updating Notion page {page_id}: {e}")