import numpy as np
import pandas as pd


def analyze_data(df):

    print("\n==============================")
    print("NUMPY + PANDAS ANALYSIS")
    print("==============================")


    # ==================================================
    # 1. Basic statistics using NumPy
    # ==================================================

    scores = df["score"].to_numpy()

    comments = df["num_comments"].to_numpy()


    average_score = np.mean(scores)

    median_score = np.median(scores)

    score_std = np.std(scores)

    max_score = np.max(scores)

    min_score = np.min(scores)


    average_comments = np.mean(comments)


    print("\nScore Statistics")

    print(
        f"Mean:   {average_score:.2f}"
    )

    print(
        f"Median: {median_score:.2f}"
    )

    print(
        f"Std:    {score_std:.2f}"
    )

    print(
        f"Maximum: {max_score}"
    )

    print(
        f"Minimum: {min_score}"
    )


    print(
        f"\nAverage comments: "
        f"{average_comments:.2f}"
    )


    # ==================================================
    # 2. Most common category using Pandas
    # ==================================================

    category_counts = (
        df["category"]
        .value_counts()
    )


    most_common_category = (
        category_counts.idxmax()
    )


    print(
        "\nMost common category:",
        most_common_category
    )


    print("\nCategory distribution:")

    print(category_counts)


    # ==================================================
    # 3. Most commented story
    # ==================================================

    most_commented_index = (
        df["num_comments"].idxmax()
    )


    most_commented_story = df.loc[
        most_commented_index
    ]


    print("\nMost commented story:")

    print(
        most_commented_story["title"]
    )

    print(
        "Comments:",
        most_commented_story["num_comments"]
    )


    # ==================================================
    # 4. Most popular story
    # ==================================================

    most_popular_index = (
        df["score"].idxmax()
    )


    most_popular_story = df.loc[
        most_popular_index
    ]


    print("\nHighest scored story:")

    print(
        most_popular_story["title"]
    )

    print(
        "Score:",
        most_popular_story["score"]
    )


    # ==================================================
    # 5. Engagement feature
    # ==================================================

    df["engagement"] = (
        df["num_comments"]
        / (df["score"] + 1)
    )


    # ==================================================
    # 6. Popularity flag
    # ==================================================

    df["is_popular"] = (
        df["score"] > average_score
    )


    # ==================================================
    # 7. Engagement ranking
    # ==================================================

    df["engagement_rank"] = (
        df["engagement"]
        .rank(
            ascending=False,
            method="min"
        )
        .astype(int)
    )


    # ==================================================
    # 8. Category-level analysis
    # ==================================================

    category_analysis = (
        df.groupby("category")
        .agg(
            articles=("post_id", "count"),
            average_score=("score", "mean"),
            average_comments=(
                "num_comments",
                "mean"
            ),
            average_engagement=(
                "engagement",
                "mean"
            )
        )
        .sort_values(
            "average_score",
            ascending=False
        )
    )


    print(
        "\nCategory Analysis:"
    )

    print(
        category_analysis
    )


    # ==================================================
    # 9. NumPy percentile analysis
    # ==================================================

    score_75th_percentile = np.percentile(
        scores,
        75
    )

    print(
        "\n75th percentile score:",
        score_75th_percentile
    )


    # Stories above the 75th percentile
    high_performers = df[
        df["score"] >= score_75th_percentile
    ]


    print(
        "High-performing stories:",
        len(high_performers)
    )


    # ==================================================
    # 10. Create summary
    # ==================================================

    summary = {

        "total_articles": len(df),

        "average_score": average_score,

        "median_score": median_score,

        "score_std": score_std,

        "max_score": max_score,

        "min_score": min_score,

        "average_comments": average_comments,

        "most_common_category":
            most_common_category,

        "most_commented_story":
            most_commented_story["title"],

        "most_commented_count":
            int(
                most_commented_story[
                    "num_comments"
                ]
            ),

        "highest_scored_story":
            most_popular_story["title"],

        "highest_score":
            int(
                most_popular_story["score"]
            ),

        "75th_percentile_score":
            score_75th_percentile
    }


    return df, category_analysis, summary