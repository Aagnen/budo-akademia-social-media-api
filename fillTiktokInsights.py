import config
import asyncio
from methods import notionMethods
from methods import tiktokMethods
from methods.logger import logger

async def main():
    # Step 1: Fetch TikTok feed insights
    try:
        logger.info("🚀 Starting TikTok feed fetching process...")
        tiktok_insights = await tiktokMethods.get_tiktok_feed()
        logger.info("✅ Successfully fetched TikTok feed insights.")
    except Exception as e:
        logger.error(f"⛔ An error occurred: {e}")

    #tiktokpy turns-off logger :P 

    # Step 2: Fetch entries from Notion
    logger.info("🚀 Starting Notion entries fetch...")
    entries = notionMethods.get_notion_entries_with_property(config.NOTION_DATABASE_ID, "TiktokId")
    logger.info(f"✅ Found {len(entries)} entries with TiktokId.")

    # Step 3: Process Notion entries
    for entry in entries:
        page_id = entry['id']
        properties = entry['properties']
        tiktok_id_property = properties.get('TiktokId', {})
        tiktok_id_text = tiktok_id_property.get('rich_text', [])
        
        if tiktok_id_text:
            tiktok_id = tiktok_id_text[0]['plain_text']
            logger.info(f"▶️ Processing TiktokId: {tiktok_id}")

            # Match insights with TiktokId
            matching_insight = next((insight for insight in tiktok_insights if insight["Video ID"] == tiktok_id), None)
            if matching_insight:
                # Update Notion entry with the insights
                success = notionMethods.update_notion_entry_with_insights(page_id, matching_insight, platform='TikTok')
                if success:
                    logger.info(f"✅ Updated Notion entry {page_id} with TikTok insights.")
                else:
                    logger.error(f"⛔ Failed to update Notion entry {page_id} for TiktokId {tiktok_id}.")
            else:
                logger.warning(f"No insights available for TiktokId {tiktok_id}.")
        else:
            logger.warning(f"No TiktokId found for page {page_id}. Skipping.")

if __name__ == "__main__":
    asyncio.run(main())
