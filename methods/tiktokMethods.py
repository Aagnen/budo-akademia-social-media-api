import logging
import asyncio
from tiktokpy import TikTokPy
from .logger import logger

async def login():
    """
    Logs into TikTok using TikTokPy's login_session method.
    """
    async with TikTokPy() as bot:
        await bot.login_session()
    logger.info("🔑 Logged in successfully.")

async def fetch_feed(bot):
    """
    Fetches the TikTok feed for the specified user.

    Args:
        bot (TikTokPy): An instance of the TikTokPy bot.

    Returns:
        List[dict]: A list of dictionaries containing video insights.
    """
    user_feed_items = await bot.user_feed(username="@budoakademia", amount=9)
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
        logger.info(f"▶️ Video ID: {item.id} | Plays: {item.stats.plays}")
    return insights

async def get_tiktok_feed():
    """
    Fetches the TikTok feed for a specific user and gathers insights.
    If not logged in, it logs in and retries.

    Returns:
        List[dict]: A list of dictionaries containing video insights.
    """
    logger.info("Inside get_tiktok_feed()- 1")
    max_attempts = 2  # Max number of attempts to fetch the feed
    attempt = 0
    logger.info("Inside get_tiktok_feed()- 2")
    while attempt < max_attempts:
        try:
            async with TikTokPy() as bot:
                insights = await fetch_feed(bot)
                logger.info("Inside get_tiktok_feed()- 3")
                return insights
        except Exception as e:
            attempt += 1
            logger.error(f"⚠️ Error fetching TikTok feed: {e}")
            if attempt < max_attempts:
                logger.info("🔐 Attempting to log in and retry...")
                await login()
            else:
                logger.error("⛔ Max attempts reached. Failed to fetch TikTok feed.")
                raise e  # Re-raise the exception after max attempts

async def main():
    """
    Main function to execute the TikTok feed fetching process.
    """
    try:
        logger.info("🚀 Starting TikTok feed fetching process...")
        insights = await get_tiktok_feed()
        # Process the insights as needed
        logger.info("✅ Successfully fetched TikTok feed insights.")
    except Exception as e:
        logger.error(f"⛔ An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
