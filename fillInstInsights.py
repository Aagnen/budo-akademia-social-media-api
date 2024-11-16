import config
from methods import methodsNotion
from methods import methodsInstagram

entries = methodsNotion.get_notion_entries_with_instid(config.NOTION_DATABASE_ID)
print(f"Found {len(entries)} entries with InstId.")

for entry in entries:
    page_id = entry['id']
    properties = entry['properties']
    inst_id_property = properties.get('InstId', {})
    inst_id_text = inst_id_property.get('rich_text', [])
    if inst_id_text:
        inst_id = inst_id_text[0]['plain_text']
        print(f"Processing InstId: {inst_id}")

        insights = methodsInstagram.fetch_post_insights(inst_id)

        if insights:
            methodsNotion.update_notion_entry_with_insights(page_id, insights)
        else:
            print(f"   No insights available for InstId {inst_id}.")
    else:
        print(f"   No InstId found for page {page_id}. Skipping.")
