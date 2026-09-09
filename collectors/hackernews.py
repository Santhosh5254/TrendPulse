import requests
import re

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


TOP_STORIES_URL = (
    "https://hacker-news.firebaseio.com/v0/topstories.json"
)

ITEM_URL = (
    "https://hacker-news.firebaseio.com/v0/item/{}.json"
)


HEADERS = {
    "User-Agent": "TrendPulse/1.0"
}


KEYWORDS = {

    "technology": [
        "AI",
        "software",
        "tech",
        "code",
        "computer",
        "data",
        "cloud",
        "API",
        "GPU",
        "LLM"
    ],

    "worldnews": [
        "war",
        "government",
        "country",
        "president",
        "election",
        "climate",
        "attack",
        "global"
    ],

    "sports": [
        "NFL",
        "NBA",
        "FIFA",
        "sport",
        "team",
        "player",
        "league",
        "championship"
    ],

    "science": [
        "research",
        "study",
        "space",
        "physics",
        "biology",
        "discovery",
        "NASA",
        "genome"
    ],

    "entertainment": [
        "movie",
        "film",
        "music",
        "Netflix",
        "book",
        "show",
        "award",
        "streaming"
    ]
}


def matches_category(title, keywords):

    for keyword in keywords:

        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(
            pattern,
            title,
            re.IGNORECASE
        ):
            return True

    return False


def fetch_story(story_id):
    """
    Fetch one Hacker News story.
    This function is executed concurrently.
    """

    try:

        response = requests.get(
            ITEM_URL.format(story_id),
            headers=HEADERS,
            timeout=5
        )

        response.raise_for_status()

        story = response.json()

        if not story:
            return None

        if story.get("type") != "story":
            return None

        title = story.get("title")

        if not title:
            return None

        return story

    except requests.RequestException:

        return None


def fetch_hackernews():

    print("Fetching Hacker News story IDs...")

    try:

        response = requests.get(
            TOP_STORIES_URL,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        story_ids = response.json()

    except requests.RequestException as error:

        print(
            f"Failed to fetch story IDs: {error}"
        )

        return []


    print(
        f"✓ Received {len(story_ids)} story IDs"
    )


    # Analyze latest 200 stories.
    story_ids = story_ids[:200]


    print(
        f"Fetching {len(story_ids)} stories concurrently..."
    )


    stories = []


    # --------------------------------------------------
    # Fetch stories concurrently
    # --------------------------------------------------

    with ThreadPoolExecutor(
        max_workers=20
    ) as executor:

        futures = [
            executor.submit(
                fetch_story,
                story_id
            )
            for story_id in story_ids
        ]


        for index, future in enumerate(
            as_completed(futures),
            start=1
        ):

            story = future.result()

            if story:
                stories.append(story)


            if index % 20 == 0:

                print(
                    f"Fetched {index}/"
                    f"{len(story_ids)} stories"
                )


    print(
        f"✓ Successfully fetched "
        f"{len(stories)} stories"
    )


    # --------------------------------------------------
    # Categorize stories
    # --------------------------------------------------

    results = {
        category: []
        for category in KEYWORDS
    }


    collected_at = datetime.now().isoformat()


    for story in stories:

        title = story.get("title", "").strip()


        for category, keywords in KEYWORDS.items():

            if len(results[category]) >= 25:
                continue


            if matches_category(
                title,
                keywords
            ):

                article = {

                    "post_id":
                        story.get("id"),

                    "title":
                        title,

                    "category":
                        category,

                    "score":
                        story.get("score", 0),

                    "num_comments":
                        story.get(
                            "descendants",
                            0
                        ),

                    "author":
                        story.get("by"),

                    "collected_at":
                        collected_at
                }


                results[category].append(
                    article
                )

                # One story belongs to one category.
                break


    # --------------------------------------------------
    # Combine categories
    # --------------------------------------------------

    articles = []


    for category, items in results.items():

        print(
            f"{category}: "
            f"{len(items)} stories"
        )

        articles.extend(items)


    print(
        f"✓ Total articles collected: "
        f"{len(articles)}"
    )


    return articles