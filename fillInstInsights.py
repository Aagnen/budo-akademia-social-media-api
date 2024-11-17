import config
from methods import notionMethods
from methods import instagramMethods
from methods.logger import logger

# Retrieve entries from Notion where 'InstId' property is not empty
entries = notionMethods.get_notion_entries_with_property(config.NOTION_DATABASE_ID, "InstId")
logger.info(f"Found {len(entries)} entries with InstId.")

for entry in entries:
    page_id = entry['id']
    properties = entry['properties']
    inst_id_property = properties.get('InstId', {})
    inst_id_text = inst_id_property.get('rich_text', [])
    if inst_id_text:
        inst_id = inst_id_text[0]['plain_text']
        logger.debug(f"🚀 Processing InstId: {inst_id}")

        # Fetch insights for the Instagram post
        insights = instagramMethods.fetch_post_insights(inst_id)

        if insights:
            # Update the Notion page with the insights
            success = notionMethods.update_notion_entry_with_insights(page_id, insights, platform='Instagram')
            if success:
                logger.info(f"✅ Done InstId: {inst_id}")
            else:
                logger.error(f"Failed to update page {page_id} for InstId {inst_id}.")
        else:
            logger.warning(f"No insights available for InstId {inst_id}.")
    else:
        logger.warning(f"No InstId found for page {page_id}. Skipping.")
