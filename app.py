import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

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

# ---------- Premium styling ----------
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #07111f 0%, #0a1628 100%);
        }

        .main-title {
            font-size: 3rem;
            font-weight: 800;
            color: #f5f7fb;
            margin-bottom: 0.2rem;
        }

        .sub-title {
            color: #a9b7cc;
            font-size: 1.05rem;
            margin-bottom: 1rem;
        }

        .hero-box {
            background: linear-gradient(135deg, #132845 0%, #183457 100%);
            border: 1px solid rgba(138, 180, 248, 0.18);
            padding: 1rem 1.25rem;
            border-radius: 16px;
            color: #d8e6ff;
            margin-bottom: 1rem;
        }

        .section-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 18px;
            padding: 1rem 1rem 0.5rem 1rem;
            margin-bottom: 1rem;
        }

        .small-note {
            color: #9fb0c9;
            font-size: 0.95rem;
        }

        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            padding: 14px;
            border-radius: 16px;
        }

        div[data-testid="stMetricLabel"] {
            color: #9fb0c9;
        }

        div[data-testid="stMetricValue"] {
            color: #f5f7fb;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown('<div class="main-title">SpendIQ 💸</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">AI-powered insights to help you spend smarter and build wealth</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="hero-box">
        📊 Understand your spending.  🤖 Get AI insights.  💡 Make better financial decisions.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Input mode ----------
input_mode = st.radio(
    "Choose how to input data",
    ["Upload File", "Manual Entry"],
    horizontal=False,
)

uploaded_file = None
df = None

if input_mode == "Upload File":
    uploaded_file = st.file_uploader(
        "Upload your transaction CSV or Excel",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        df = load_data(uploaded_file)

elif input_mode == "Manual Entry":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Add Transaction")

    with st.form("manual_entry_form"):
        col1, col2 = st.columns(2)

        date = col1.date_input("Date")
        amount = col2.number_input("Amount", min_value=0.0, format="%.2f")

        description = st.text_input("Description")
        category = st.selectbox(
            "Category",
            ["Groceries", "Shopping", "Gas", "Food", "Subscription", "Other"]
        )

        submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if description.strip() and amount > 0:
            df = pd.DataFrame([{
                "date": date,
                "description": description.strip(),
                "amount": amount,
                "category": category
            }])
        else:
            st.warning("Enter a description and an amount greater than 0.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Processing + UI ----------
if df is not None:
    try:
        df = clean_transactions(df)

        monthly_df = monthly_summary(df)
        category_df = category_summary(df)
        top_txn_df = top_transactions(df).copy()

        # Biggest opportunity
        st.markdown("## 💡 Your Biggest Opportunity")
        top_category = None
        potential_savings = 0

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

            a, b = st.columns(2)
            c, d = st.columns(2)

            with a:
                st.markdown("#### 📊 Summary")
                st.info(summary_text if summary_text else "No summary available.")

            with b:
                st.markdown("#### 🔍 Key Insight")
                st.info(key_insight_text if key_insight_text else "No key insight available.")

            with c:
                st.markdown("#### 💡 Recommendation")
                st.warning(recommendation_text if recommendation_text else "No recommendation available.")

            with d:
                st.markdown("#### ✨ Mindset Tip")
                st.success(mindset_tip_text if mindset_tip_text else "No mindset tip available.")

        st.markdown("---")

        # Charts
        st.markdown("## 📉 Spending Analysis")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("### Monthly Spending")
            fig1, ax1 = plt.subplots(figsize=(8, 4))
            ax1.plot(monthly_df["month"], monthly_df["amount"], marker="o")
            ax1.set_xlabel("Month")
            ax1.set_ylabel("Amount")
            ax1.set_title("Monthly Spending Trend")
            plt.xticks(rotation=45)
            st.pyplot(fig1)

        with chart_col2:
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
        df["date"] = df["date"].dt.date
        top_txn_df["date"] = top_txn_df["date"].dt.date

        st.markdown("### 💸 Top Transactions")
        st.dataframe(top_txn_df, use_container_width=True)

        st.markdown("### 📋 Full Transaction Details")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing file: {e}")

elif input_mode == "Upload File":
    st.info("Upload a CSV or Excel file to begin.")

elif input_mode == "Manual Entry":
    st.info("Enter a transaction and click 'Add Transaction' to begin.")