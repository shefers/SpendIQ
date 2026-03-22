def generate_basic_insights(df, category_df, monthly_df):
    insights = []

    if not category_df.empty:
        top_cat = category_df.iloc[0]
        insights.append(
            f"Your highest spending category is '{top_cat['category']}' at ${top_cat['amount']:.2f}."
        )

    if len(monthly_df) >= 2:
        latest = monthly_df.iloc[-1]["amount"]
        previous = monthly_df.iloc[-2]["amount"]

        if previous != 0:
            pct_change = ((latest - previous) / previous) * 100
            if pct_change > 0:
                insights.append(
                    f"Your spending increased by {pct_change:.1f}% compared to the previous month."
                )
            else:
                insights.append(
                    f"Your spending decreased by {abs(pct_change):.1f}% compared to the previous month."
                )

    food_like = category_df[
        category_df["category"].str.lower().isin(["food", "dining", "restaurants", "takeout"])
    ]
    if not food_like.empty:
        amt = food_like["amount"].sum()
        insights.append(f"You spent ${amt:.2f} on food-related purchases.")

    return insights