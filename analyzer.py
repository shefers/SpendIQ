import pandas as pd


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("month", as_index=False)["amount"]
        .sum()
        .sort_values("month")
    )


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )


def top_transactions(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return df.sort_values("amount", ascending=False).head(n)


def future_value_of_recurring_spend(
    monthly_amount: float,
    annual_return: float = 0.08,
    years: int = 10
) -> float:
    monthly_rate = annual_return / 12
    months = years * 12
    fv = monthly_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    return round(fv, 2)