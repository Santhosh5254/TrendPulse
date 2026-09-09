import matplotlib.pyplot as plt
import numpy as np
import os

def create_charts(
    df,
    category_analysis,
    output_dir="outputs"
):
    os.makedirs(output_dir, exist_ok=True)
    print("\n==============================")
    print("CREATING VISUALIZATIONS")
    print("==============================")


    # ==================================================
    # Chart 1: Top 10 Stories by Score
    # ==================================================

    top_stories = (
        df.sort_values(
            "score",
            ascending=False
        )
        .head(10)
        .sort_values(
            "score"
        )
    )


    plt.figure(
        figsize=(10, 6)
    )


    plt.barh(
        top_stories["title"],
        top_stories["score"]
    )


    plt.xlabel(
        "Hacker News Score"
    )

    plt.ylabel(
        "Story"
    )

    plt.title(
        "Top 10 Stories by Score"
    )


    plt.tight_layout()


    plt.savefig(
        f"{output_dir}/chart1_top_stories.png",
        dpi=150,
        bbox_inches="tight"
    )


    plt.show()

    plt.close()


    # ==================================================
    # Chart 2: Articles by Category
    # ==================================================

    category_counts = (
        df["category"]
        .value_counts()
    )


    plt.figure(
        figsize=(9, 6)
    )


    # NumPy generates positions for the bars
    positions = np.arange(
        len(category_counts)
    )


    plt.bar(
        positions,
        category_counts.values
    )


    plt.xticks(
        positions,
        category_counts.index
    )


    plt.xlabel(
        "Category"
    )

    plt.ylabel(
        "Number of Articles"
    )

    plt.title(
        "Article Distribution by Category"
    )


    plt.tight_layout()


    plt.savefig(
        f"{output_dir}/chart2_categories.png",
        dpi=150,
        bbox_inches="tight"
    )


    plt.show()

    plt.close()


    # ==================================================
    # Chart 3: Score vs Comments
    # ==================================================

    plt.figure(
        figsize=(9, 6)
    )


    plt.scatter(
        df["score"],
        df["num_comments"],
        alpha=0.7
    )


    plt.xlabel(
        "Score"
    )

    plt.ylabel(
        "Comments"
    )

    plt.title(
        "Story Score vs Number of Comments"
    )


    # Add mean reference lines
    mean_score = np.mean(
        df["score"]
    )

    mean_comments = np.mean(
        df["num_comments"]
    )


    plt.axvline(
        mean_score,
        linestyle="--",
        label="Mean Score"
    )


    plt.axhline(
        mean_comments,
        linestyle="--",
        label="Mean Comments"
    )


    plt.legend()


    plt.tight_layout()


    plt.savefig(
        f"{output_dir}/chart3_score_vs_comments.png",
        dpi=150,
        bbox_inches="tight"
    )


    plt.show()

    plt.close()


    print("\n✓ Charts created successfully.")

    print(
        f"Saved to: {output_dir}/"
    )