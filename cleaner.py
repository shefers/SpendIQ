import pandas as pd


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.strip().lower() for col in df.columns]

    required_cols = ["date", "description", "amount"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["description"] = df["description"].astype(str).str.strip()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna(subset=["date", "description", "amount"])
    df["type"] = df["amount"].apply(lambda x: "Expense" if x > 0 else "Income")

    if "category" not in df.columns:
        df["category"] = "Uncategorized"
    else:
        df["category"] = df["category"].fillna("Uncategorized")

    df["month"] = df["date"].dt.to_period("M").astype(str)

    return df
