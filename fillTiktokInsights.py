import config
import asyncio
from tiktokpy import TikTokPy
from methods import methodsNotion
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_tiktok_feed():
    """
    Fetch the TikTok feed for a specific user and gather insights.

    Returns:
        List[dict]: A list of dictionaries containing video insights.
    """
    async with TikTokPy() as bot:
        user_feed_items = await bot.user_feed(username="@budoakademia", amount=20)
        insights = []
        for item in user_feed_items:
            # Gather insights
            insight = {
                "Video ID": item.id,
                "Plays": item.stats.plays,
                "Shares": item.stats.shares,
                "Likes": item.stats.likes,
            }
            insights.append(insight)
            # Log video stats
            logger.info(f"Video ID: {item.id} | Plays: {item.stats.plays}")
        return insights

async def main():
    # Step 1: Fetch TikTok feed insights
    logger.info("Fetching TikTok feed...")
    tiktok_insights = await get_tiktok_feed()

    # Step 2: Fetch entries from Notion
    entries = methodsNotion.get_notion_entries_with_property(config.NOTION_DATABASE_ID, "TiktokId")
    logger.info(f"Found {len(entries)} entries with TiktokId.")

    # Step 3: Process Notion entries
    for entry in entries:
        page_id = entry['id']
        properties = entry['properties']
        tiktok_id_property = properties.get('TiktokId', {})
        tiktok_id_text = tiktok_id_property.get('rich_text', [])
        
        if tiktok_id_text:
            tiktok_id = tiktok_id_text[0]['plain_text']
            logger.info(f"Processing TiktokId: {tiktok_id}")

            # Match insights with TiktokId
            matching_insight = next((insight for insight in tiktok_insights if insight["Video ID"] == tiktok_id), None)
            if matching_insight:
                # Update Notion entry with the insights
                success = methodsNotion.update_notion_entry_with_insights(page_id, matching_insight, platform='TikTok')
                if success:
                    logger.info(f"Updated Notion entry {page_id} with TikTok insights.")
                else:
                    logger.error(f"Failed to update Notion entry {page_id} for TiktokId {tiktok_id}.")
            else:
                logger.warning(f"No insights available for TiktokId {tiktok_id}.")
        else:
            logger.warning(f"No TiktokId found for page {page_id}. Skipping.")

if __name__ == "__main__":
    asyncio.run(main())
