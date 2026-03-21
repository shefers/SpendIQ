import streamlit as st
import matplotlib.pyplot as plt

from data_loader import load_data
from cleaner import clean_transactions
from analyzer import (
    monthly_summary,
    category_summary,
    top_transactions,
    future_value_of_recurring_spend,
)
from insights import generate_basic_insights
from ai_insights import generate_ai_insight


st.set_page_config(page_title="SpendIQ", layout="wide")

# Header
st.title("SpendIQ 💸")
st.caption("AI-powered insights to help you spend smarter and build wealth")
st.info("📊 Understand your spending. 🤖 Get AI insights. 💡 Make better financial decisions.")

uploaded_file = st.file_uploader("Upload your transaction CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Load and clean data
        df = load_data(uploaded_file)
        df = clean_transactions(df)

        # Build summaries
        monthly_df = monthly_summary(df)
        category_df = category_summary(df)
        top_txn_df = top_transactions(df)

        # Big insight banner
        st.markdown("## 💡 Your Biggest Opportunity")
        top_category = None

        if not category_df.empty:
            top_category = category_df.iloc[0]
            potential_savings = top_category["amount"] * 0.2

            st.error(
                f"You are spending the most on {top_category['category']} "
                f"(${top_category['amount']:.0f}). Reducing this by 20% could save you about "
                f"${potential_savings:.0f}."
            )
        else:
            st.info("Upload more transaction data to unlock your biggest opportunity insight.")

        st.markdown("---")

        # Metrics
        total_spend = df["amount"].sum()
        avg_monthly = monthly_df["amount"].mean() if not monthly_df.empty else 0
        score = max(0, 100 - (total_spend / 100))

        st.markdown("## 📊 Financial Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Spend", f"${total_spend:,.2f}")
        col2.metric("Average Monthly Spend", f"${avg_monthly:,.2f}")
        col3.metric("Transactions", f"{len(df)}")
        col4.metric("Financial Health Score", f"{score:.0f}/100")

        # Savings opportunity
        if top_category is not None:
            st.markdown("### 💰 Savings Opportunity")
            st.success(
                f"If you reduce your {top_category['category']} spending by 20%, "
                f"you could save approximately ${potential_savings:.0f}."
            )

        st.markdown("---")

        # AI Coach
        st.markdown("## 🤖 SpendIQ Coach")
        st.caption("Get a simple AI-generated summary of your spending patterns.")

        if st.button("Generate AI Insight"):
            with st.spinner("Analyzing your spending..."):
                insight = generate_ai_insight(df, category_df, monthly_df)

            summary_text = ""
            key_insight_text = ""
            recommendation_text = ""
            mindset_tip_text = ""

            sections = insight.split("\n\n")

            for section in sections:
                section_clean = section.strip()
                section_lower = section_clean.lower()

                if section_lower.startswith("summary:"):
                    summary_text = section_clean.replace("Summary:", "", 1).strip()

                elif section_lower.startswith("key insight:"):
                    key_insight_text = section_clean.replace("Key Insight:", "", 1).strip()

                elif section_lower.startswith("recommendation:"):
                    recommendation_text = section_clean.replace("Recommendation:", "", 1).strip()

                elif section_lower.startswith("mindset tip:"):
                    mindset_tip_text = section_clean.replace("Mindset Tip:", "", 1).strip()

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            with col1:
                st.markdown("#### 📊 Summary")
                st.info(summary_text if summary_text else "No summary available.")

            with col2:
                st.markdown("#### 🔍 Key Insight")
                st.info(key_insight_text if key_insight_text else "No key insight available.")

            with col3:
                st.markdown("#### 💡 Recommendation")
                st.warning(recommendation_text if recommendation_text else "No recommendation available.")

            with col4:
                st.markdown("#### ✨ Mindset Tip")
                st.success(mindset_tip_text if mindset_tip_text else "No mindset tip available.")

        st.markdown("---")

        # Charts
        st.markdown("## 📉 Spending Analysis")

        st.markdown("### Monthly Spending")
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        ax1.plot(monthly_df["month"], monthly_df["amount"], marker="o")
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Amount")
        ax1.set_title("Monthly Spending Trend")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

        st.markdown("### Spending by Category")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.bar(category_df["category"], category_df["amount"])
        ax2.set_xlabel("Category")
        ax2.set_ylabel("Amount")
        ax2.set_title("Category Spend")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

        st.markdown("---")

        # Future value calculator
        st.markdown("## 💸 Future Cost Calculator")
        monthly_amount = st.number_input(
            "Enter recurring monthly spend",
            min_value=0.0,
            value=100.0,
            step=10.0
        )
        annual_return = st.slider(
            "Expected annual return (%)",
            min_value=1,
            max_value=15,
            value=8
        ) / 100
        years = st.slider("Years", min_value=1, max_value=30, value=10)

        future_cost = future_value_of_recurring_spend(
            monthly_amount,
            annual_return,
            years
        )

        st.success(
            f"If you invested ${monthly_amount:.2f}/month instead, "
            f"it could grow to approximately ${future_cost:,.2f} in {years} years."
        )

        st.markdown("---")

        # Rule-based insights
        st.markdown("## 🧠 Insights")
        insights = generate_basic_insights(df, category_df, monthly_df)
        for insight in insights:
            st.write(f"- {insight}")

        st.markdown("---")

        # Transactions
        st.markdown("## 📄 Transactions")

        df = df.copy()
        top_txn_df = top_txn_df.copy()

        df["date"] = df["date"].dt.date
        top_txn_df["date"] = top_txn_df["date"].dt.date

        st.markdown("### Top Transactions")
        st.dataframe(top_txn_df, use_container_width=True)

        st.markdown("### Full Transaction Details")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Upload a CSV file to begin.")