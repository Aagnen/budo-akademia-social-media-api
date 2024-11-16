import config
from methods import methodsNotion
from methods import methodsInstagram

posts = methodsInstagram.fetch_all_posts(config.INSTAGRAM_USER_ID)

for post in posts:
    inst_id = post.get('id')
    caption = post.get('caption')
    timestamp = post.get('timestamp')
    print(f'Processing InstId: {inst_id}')
    
    if not methodsNotion.if_page_exists(inst_id, config.NOTION_DATABASE_ID):
        methodsNotion.create_notion_page(inst_id, caption, timestamp, config.NOTION_DATABASE_ID)
        print(f'   All completed for InstId: {inst_id}')
    else:
        print(f'   Page for InstId {inst_id} already exists. Skipping.')