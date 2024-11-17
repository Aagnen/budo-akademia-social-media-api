import config
import asyncio
from tiktokpy import TikTokPy
from methods import methodsNotion

async def get_tiktok_feed():
    # Fetch TikTok feed
    async with TikTokPy() as bot:
        user_feed_items = await bot.user_feed(username="@budoakademia", amount=9)
        insights = []  # Initialize insights list
        for item in user_feed_items:
            # Gather insights
            insight = {
                "Video ID": item.id,
                "Plays": item.stats.plays,
                "Shares": item.stats.shares,
                "Likes": item.stats.likes,
            }
            insights.append(insight)
            # Print video stats
            print(f"Video ID: {item.id} | Plays: {item.stats.plays}")
        return insights

async def main():
    # Step 1: Fetch TikTok feed insights
    print("Fetching TikTok feed...")
    tiktok_insights = await get_tiktok_feed()

    # Step 2: Fetch entries from Notion
    entries = methodsNotion.get_notion_entries_with_property(config.NOTION_DATABASE_ID, "TiktokId")
    print(f"Found {len(entries)} entries with TiktokId.")

    # Step 3: Process Notion entries
    for entry in entries:
        page_id = entry['id']
        properties = entry['properties']
        tikTok_id_property = properties.get('TiktokId', {})
        tikTok_id_text = tikTok_id_property.get('rich_text', [])
        
        if tikTok_id_text:
            tikTok_id = tikTok_id_text[0]['plain_text']
            print(f"Processing TiktokId: {tikTok_id}")

            # Match insights with InstId
            matching_insight = next((insight for insight in tiktok_insights if insight["Video ID"] == tikTok_id), None)
            if matching_insight:
                methodsNotion.update_notion_entry_with_Tiktok_insights(page_id, matching_insight)
                print(f"   Updated Notion entry {page_id} with TikTok insights.")
            else:
                print(f"   No insights available for InstId {tikTok_id}.")
        else:
            print(f"   No InstId found for page {page_id}. Skipping.")

if __name__ == "__main__":
    asyncio.run(main())
