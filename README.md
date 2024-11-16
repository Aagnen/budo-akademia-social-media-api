# Budo Akademia Social Media API

This repository provides an API for automating interactions between Instagram and Notion. The purpose of this project is to extract insights from Instagram posts and update them in a Notion database, facilitating streamlined social media analytics.

## Features

- Fetch posts and insights from Instagram via the Meta Graph API.
- Update Notion database entries with Instagram post data and insights.
- Automatically create new Notion entries for Instagram posts when they don't already exist.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Aagnen/budo-akademia-social-media-api.git
   cd budo-akademia-social-media-api
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Create private Notion Plugin, according to the instructions from Notion Api and connect it to your chosen database.
4. Make sure the database has all fields you want to update, especially "InstId" for Instagram Id.
5. Set up a `config.py` file in the root directory with the following details:

```python
   INSTAGRAM_ACCESS_TOKEN = "your-instagram-access-token"
   INSTAGRAM_USER_ID = "your-instagram-user-id"
   NOTION_API_TOKEN = "your-notion-api-token"
   NOTION_DATABASE_ID = "your-notion-database-id"
```

## How It Works

### Instagram Insights Fetching

The script fetches insights such as reach, likes, saves, and shares for Instagram posts. It uses the [Meta Graph API](https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights) to access Instagram media insights.

**How to Obtain Instagram Access Token**

- Use the Meta Graph API Explorer: [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/).

### Notion Integration

The Notion API is used to create, update, and query entries in a Notion database. You can find the Notion API documentation [here](https://developers.notion.com/docs/getting-started).

## Main Scripts

### 1. `fillInstInsights.py`

Fetches insights for Instagram posts and updates existing Notion entries.

### 2. `populateNotionDB.py`

Populates the Notion database with new Instagram posts if they don't already exist.

### 3. `methods/methodsInstagram.py`

Handles Instagram API calls, such as fetching posts and insights.

### 4. `methods/methodsNotion.py`

Handles Notion API calls for creating, updating, and querying database entries.

## Running the Scripts

- To populate the Notion database with Instagram posts:

  ```bash
  python populateNotionDB.py
  ```
- To update existing Notion entries with Instagram insights:

  ```bash
  python fillInstInsights.py
  ```

## Documentation

- Instagram API Documentation: [Instagram Media Insights](https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights)
- Notion API Documentation: [Notion API](https://developers.notion.com/docs/getting-started)
