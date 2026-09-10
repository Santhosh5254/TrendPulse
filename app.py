from flask import Flask, render_template, jsonify, request
import time
import os

from collectors.hackernews import fetch_hackernews
from processing.cleaner import clean_data
from analysis.analyzer import analyze_data


app = Flask(__name__)


# ==================================================
# Cache configuration
# ==================================================

CACHE_DURATION = 5 * 60  # 5 minutes

cached_result = None
cached_at = 0
cached_feed = None


# ==================================================
# CSV configuration
# ==================================================

SAVE_CSV = (
    os.getenv("SAVE_CSV", "true").lower() == "true"
    and os.getenv("VERCEL") != "1"
)


# ==================================================
# Create data directory
# ==================================================

if SAVE_CSV:

    os.makedirs(
        "data",
        exist_ok=True
    )


# ==================================================
# Home page
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# Analyze Hacker News
# ==================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    global cached_result
    global cached_at
    global cached_feed

    current_time = time.time()


    # --------------------------------------------------
    # Get selected Hacker News feed
    # --------------------------------------------------

    data = request.get_json(silent=True) or {}

    feed_type = data.get(
        "feed",
        "top"
    )


    # Allow only supported feeds

    allowed_feeds = {

        "top",
        "new",
        "best",
        "ask",
        "show",
        "jobs"
    }


    if feed_type not in allowed_feeds:

        feed_type = "top"


    # --------------------------------------------------
    # Check cache
    # --------------------------------------------------

    if (
        cached_result is not None
        and cached_feed == feed_type
        and current_time - cached_at < CACHE_DURATION
    ):

        print(
            f"✓ Returning cached "
            f"{feed_type} analysis"
        )

        return jsonify(cached_result)


    try:

        # --------------------------------------------------
        # 1. Collect
        # --------------------------------------------------

        print(
            f"\nFetching fresh Hacker News "
            f"{feed_type} data..."
        )

        articles = fetch_hackernews(
            feed_type
        )


        if not articles:

            return jsonify({
                "success": False,
                "message":
                    "Failed to collect Hacker News data."
            }), 500


        # --------------------------------------------------
        # 2. Clean using Pandas
        # --------------------------------------------------

        df = clean_data(
            articles
        )


        if df.empty:

            return jsonify({
                "success": False,
                "message":
                    "No valid stories were "
                    "available for analysis."
            }), 500


        # --------------------------------------------------
        # Save cleaned data
        # --------------------------------------------------

        if SAVE_CSV:

            clean_path = (
                "data/trends_clean.csv"
            )

            df.to_csv(
                clean_path,
                index=False
            )

            print(
                f"✓ Cleaned data saved to "
                f"{clean_path}"
            )


        # --------------------------------------------------
        # 3. Analyze using NumPy + Pandas
        # --------------------------------------------------

        analyzed_df, category_analysis, summary = (
            analyze_data(df)
        )


        # --------------------------------------------------
        # Save analyzed data
        # --------------------------------------------------

        if SAVE_CSV:

            analyzed_path = (
                "data/trends_analysed.csv"
            )

            analyzed_df.to_csv(
                analyzed_path,
                index=False
            )

            print(
                f"✓ Analyzed data saved to "
                f"{analyzed_path}"
            )


        # --------------------------------------------------
        # 4. Top 10 stories
        # --------------------------------------------------

        top_stories = (
            analyzed_df
            .sort_values(
                "score",
                ascending=False
            )
            .head(10)
        )


        top_story_data = []


        for _, row in top_stories.iterrows():

            story_id = row["post_id"]

            top_story_data.append({

                "title":
                    row["title"],

                "score":
                    int(
                        row["score"]
                    ),

                "comments":
                    int(
                        row["num_comments"]
                    ),

                "category":
                    row["category"],

                "url":
                    f"https://news.ycombinator.com/"
                    f"item?id={story_id}"
            })


        # --------------------------------------------------
        # 5. Category distribution
        # --------------------------------------------------

        category_counts = (
            analyzed_df["category"]
            .value_counts()
        )


        category_data = {

            "labels":
                category_counts.index.tolist(),

            "values":
                category_counts.values.tolist()
        }


        # --------------------------------------------------
        # 6. Score vs comments
        # --------------------------------------------------

        scatter_data = []


        for _, row in analyzed_df.iterrows():

            scatter_data.append({

                "x":
                    int(
                        row["score"]
                    ),

                "y":
                    int(
                        row["num_comments"]
                    ),

                "title":
                    row["title"]
            })


        # --------------------------------------------------
        # 7. Prepare response
        # --------------------------------------------------

        result = {

            "success":
                True,

            "feed":
                feed_type,

            "analyzed_at":
                time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "summary": {

                "total_articles":
                    summary["total_articles"],

                "average_score":
                    round(
                        summary["average_score"],
                        2
                    ),

                "median_score":
                    round(
                        summary["median_score"],
                        2
                    ),

                "average_comments":
                    round(
                        summary["average_comments"],
                        2
                    ),

                "most_common_category":
                    summary[
                        "most_common_category"
                    ],

                "highest_score":
                    summary[
                        "highest_score"
                    ],

                "most_commented_count":
                    summary[
                        "most_commented_count"
                    ],

                "highest_scored_story":
                    summary[
                        "highest_scored_story"
                    ],

                "most_commented_story":
                    summary[
                        "most_commented_story"
                    ]
            },

            "top_stories":
                top_story_data,

            "charts": {

                "top_stories":
                    top_story_data,

                "categories":
                    category_data,

                "scatter":
                    scatter_data
            }
        }


        # --------------------------------------------------
        # 8. Cache
        # --------------------------------------------------

        cached_result = result

        cached_at = current_time

        cached_feed = feed_type


        print(
            f"✓ {feed_type} analysis "
            f"cached for 5 minutes"
        )


        return jsonify(
            result
        )


    except Exception as error:

        print(
            f"✗ Analysis failed: "
            f"{error}"
        )

        return jsonify({

            "success":
                False,

            "message":
                "An unexpected error occurred "
                "while analyzing Hacker News data."
        }), 500


# ==================================================
# Run application
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )