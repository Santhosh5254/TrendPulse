import pandas as pd


REQUIRED_COLUMNS = [
    "post_id",
    "title",
    "category",
    "score",
    "num_comments",
    "author",
    "collected_at"
]


def clean_data(articles):

    print("\n==============================")
    print("PANDAS DATA CLEANING")
    print("==============================")


    # --------------------------------------------------
    # 1. Convert list of dictionaries into DataFrame
    # --------------------------------------------------

    df = pd.DataFrame(articles)

    print(
        f"Initial rows: {len(df)}"
    )


    # --------------------------------------------------
    # 2. Make sure required columns exist
    # --------------------------------------------------

    for column in REQUIRED_COLUMNS:

        if column not in df.columns:

            df[column] = None


    df = df[REQUIRED_COLUMNS]


    # --------------------------------------------------
    # 3. Remove duplicate stories
    # --------------------------------------------------

    before = len(df)

    df = df.drop_duplicates(
        subset=["post_id"]
    )

    after = len(df)

    print(
        f"After duplicate removal: {after} "
        f"(removed {before - after})"
    )


    # --------------------------------------------------
    # 4. Remove rows without a title
    # --------------------------------------------------

    before = len(df)

    df = df.dropna(
        subset=["title"]
    )

    after = len(df)

    print(
        f"After removing missing titles: {after} "
        f"(removed {before - after})"
    )


    # --------------------------------------------------
    # 5. Clean title text
    # --------------------------------------------------

    df["title"] = (
        df["title"]
        .astype(str)
        .str.strip()
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
    )


    # --------------------------------------------------
    # 6. Clean category
    # --------------------------------------------------

    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
        .str.lower()
    )


    # --------------------------------------------------
    # 7. Convert numeric columns
    # --------------------------------------------------

    df["score"] = pd.to_numeric(
        df["score"],
        errors="coerce"
    )

    df["num_comments"] = pd.to_numeric(
        df["num_comments"],
        errors="coerce"
    )


    # --------------------------------------------------
    # 8. Handle missing numeric values
    # --------------------------------------------------

    df["score"] = df["score"].fillna(0)

    df["num_comments"] = (
        df["num_comments"]
        .fillna(0)
    )


    # --------------------------------------------------
    # 9. Remove invalid scores
    # --------------------------------------------------

    before = len(df)

    df = df[
    (df["score"] >= 0) &
    (df["num_comments"] >= 0)
    ]

    after = len(df)

    print(
        f"After score validation: {after} "
        f"(removed {before - after})"
    )


    # --------------------------------------------------
    # 10. Reset DataFrame index
    # --------------------------------------------------

    df = df.reset_index(
        drop=True
    )


    print("\nFinal DataFrame shape:")

    print(
        df.shape
    )


    print("\nData types:")

    print(
        df.dtypes
    )


    return df