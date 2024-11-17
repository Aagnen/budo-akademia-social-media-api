import config
from . import notionmethods
from . import instagramMethods
from methods.logger import logger

# Fetch all posts from Instagram
posts = instagramMethods.fetch_all_posts(config.INSTAGRAM_USER_ID)

for post in posts:
    inst_id = post.get('id')
    caption = post.get('caption')
    timestamp = post.get('timestamp')
    logger.info(f'Processing InstId: {inst_id}')
    
    if not notionmethods.page_exists(inst_id, config.NOTION_DATABASE_ID):
        result = notionmethods.create_notion_page(inst_id, caption, timestamp, config.NOTION_DATABASE_ID)
        if result:
            logger.info(f'All completed for InstId: {inst_id}')
        else:
            logger.error(f'Failed to create page for InstId: {inst_id}')
    else:
        logger.info(f'Page for InstId {inst_id} already exists. Skipping.')
