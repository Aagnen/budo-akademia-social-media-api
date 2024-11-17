# Budo Akademia Social Media API

This repository provides scripts and modules for automating interactions between TikTok, Instagram, and Notion. The goal of this project is to streamline social media analytics by fetching insights from TikTok and Instagram posts and updating them in a Notion database.

## Features

* **TikTok Integration:**
  * Fetch video insights from TikTok using `TikTokPy`.
  * Update Notion database entries with TikTok video data and insights.
  * Automatic login handling if not already authenticated.
* **Instagram Integration:**
  * Fetch posts and insights from Instagram via the Meta Graph API.
  * Update Notion database entries with Instagram post data and insights.
  * Automatically create new Notion entries for Instagram posts when they don't already exist.
* **Notion Integration:**
  * Create, update, and query entries in a Notion database.
  * Synchronize social media insights with Notion for unified analytics.
* **Logging:**
  * Detailed logging with timestamps, log levels, and emojis.
  * Colored console output for easy readability.
  * Centralized logging configuration for consistency across scripts.

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
3. **Configure Notion Integration**

   * Create a private Notion integration as per the [Notion API instructions](https://developers.notion.com/docs/getting-started).
   * Share your database with the integration to grant access.
   * Ensure your Notion database includes the necessary properties, especially `TiktokId` and `InstId` for TikTok and Instagram IDs, respectively.
4. Set up a `config.py` file in the root directory with the following details:

```python
INSTAGRAM_ACCESS_TOKEN = "your-instagram-access-token"
INSTAGRAM_USER_ID = "your-instagram-user-id"

NOTION_API_TOKEN = "your-notion-api-token"
NOTION_DATABASE_ID = "your-notion-database-id"

TIKTOK_USERNAME = "@your_tiktok_username"
```

## How It Works

### **TikTok Insights Fetching**

The script fetches video insights such as plays, shares, and likes for TikTok videos. It uses [`<span>TikTokPy</span>`](https://github.com/RussellLuo/tiktokpy), an asynchronous TikTok API wrapper.

**Key Points:**

* **Automatic Login Handling:** If the user is not logged in, the script will prompt for login and store session cookies for future use.
* **Asynchronous Execution:** Utilizes `asyncio` for efficient, non-blocking operations.

**How to Obtain TikTok Session Cookies:**

* The script can automatically create a session using `TikTokPy`. Follow the prompts when running the script.

### Instagram Insights Fetching

The script fetches insights such as reach, likes, saves, and shares for Instagram posts. It uses the [Meta Graph API](https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights) to access Instagram media insights.

**How to Obtain Instagram Access Token**

- Use the Meta Graph API Explorer: [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/).
- Follow the [Instagram API Authentication Guide](https://developers.facebook.com/docs/instagram-api/getting-started).

### Notion Integration

The Notion API is used to create, update, and query entries in a Notion database. You can find the Notion API documentation [here](https://developers.notion.com/docs/getting-started).

**Key Points:**

* **Database Schema:** Ensure your Notion database has properties matching the data you wish to update (e.g., `TiktokId`, `InstId`, `Likes`, `Shares`).

## Main Scripts

### **1. `fillTiktokInsights.py`**

Fetches insights for TikTok videos and updates existing Notion entries.

* **Location:** Root directory.
* **Usage:** Updates Notion database with the latest TikTok video insights.

### **2. `fillInstInsights.py`**

Fetches insights for Instagram posts and updates existing Notion entries.

* **Location:** Root directory.
* **Usage:** Updates Notion database with the latest Instagram post insights.

### **3. `populateNotionDB.py`**

Populates the Notion database with new Instagram posts if they don't already exist.

* **Location:** Root directory.
* **Usage:** Creates new entries in Notion for recent Instagram posts.

### **4. `methods/` Package**

Contains modules with methods for interacting with TikTok, Instagram, and Notion.

* **`tiktokMethods.py`:** Handles TikTok API calls, such as fetching videos and insights.
* **`instagramMethods.py`:** Handles Instagram API calls.
* **`notionMethods.py`:** Handles Notion API calls for creating, updating, and querying database entries.
* **`logger.py`:** Configures the logging system used across all scripts.

## Running the Scripts

- To populate the Notion database with Instagram posts:

  ```bash
  python populateNotionDB.py
  ```
- To update existing Notion entries with Instagram insights:

  ```bash
  python fillInstInsights.py
  ```
- Fetch and Update TikTok Insights

  ```bash
  python fillTiktokInsights.py
  ```

## Documentation

- Instagram API Documentation: [Instagram Media Insights](https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights)
- Notion API Documentation: [Notion API](https://developers.notion.com/docs/getting-started)
