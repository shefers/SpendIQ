import os
from openai import OpenAI


def generate_ai_insight(df, category_df, monthly_df):
    """
    Generate a clean AI summary of the user's spending behavior.
    Returns a formatted string with predictable section headers.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "Summary:\nAI insight is not available yet.\n\n"
            "Key Insight:\nOPENAI_API_KEY is not set.\n\n"
            "Recommendation:\nAdd your API key and try again.\n\n"
            "Mindset Tip:\nA solid setup today saves time later."
        )

    try:
        client = OpenAI(api_key=api_key)

        top_categories = category_df.head(5).to_dict(orient="records")
        monthly_trend = monthly_df.to_dict(orient="records")
        sample_transactions = df.head(10).to_dict(orient="records")

        prompt = f"""
You are a smart, practical personal finance advisor.

Analyze the user's spending data and provide high-value insights.

Focus on:
- Where money is going
- What changed over time
- What the user should DO next

Rules:
- Keep it concise and clear
- No markdown, no bullet points
- Use simple language
- Be specific and actionable
- Do NOT use asterisks
- Keep the tone professional, supportive, and concise
- Use plain English
-Be direct. Avoid vague statements. Give concrete observations.

Return your answer in EXACTLY this format:

Summary:
Brief overview of spending behavior.

Key Insight:
Most important pattern or issue.

Recommendation:
One clear action that can improve finances.

Mindset Tip:
Short motivating sentence.

Data:
Top categories: {top_categories}
Monthly trend: {monthly_trend}
Sample transactions: {sample_transactions}
"""

        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        output = response.output_text.strip()

        # Fallback formatting if the model does not follow the exact structure
        if "Summary:" not in output:
            return (
                f"Summary:\n{output}\n\n"
                "Key Insight:\nYour spending patterns show where your biggest opportunities are.\n\n"
                "Recommendation:\nFocus on reducing one flexible spending category this month.\n\n"
                "Mindset Tip:\nSmall habits can create long-term financial wins."
            )

        return output

    except Exception as e:
        error_text = str(e).lower()

        if "insufficient_quota" in error_text or "exceeded your current quota" in error_text:
            return (
                "Summary:\nAI insight is temporarily unavailable.\n\n"
                "Key Insight:\nYour OpenAI project has no remaining quota or credits.\n\n"
                "Recommendation:\nCheck your billing and usage, then try again.\n\n"
                "Mindset Tip:\nYour app is working well — this is just an account setup step."
            )

        if "invalid_api_key" in error_text or "incorrect api key" in error_text:
            return (
                "Summary:\nAI insight is temporarily unavailable.\n\n"
                "Key Insight:\nThe API key appears to be invalid.\n\n"
                "Recommendation:\nUpdate your OPENAI_API_KEY and try again.\n\n"
                "Mindset Tip:\nSetup issues happen — you're close."
            )

        if "rate_limit" in error_text:
            return (
                "Summary:\nAI insight is temporarily unavailable.\n\n"
                "Key Insight:\nToo many requests were sent in a short time.\n\n"
                "Recommendation:\nWait a moment and try again.\n\n"
                "Mindset Tip:\nA short pause is all you need."
            )

        return (
            "Summary:\nAI insight is temporarily unavailable.\n\n"
            f"Key Insight:\n{str(e)}\n\n"
            "Recommendation:\nPlease try again in a moment.\n\n"
            "Mindset Tip:\nYou're making strong progress on this app."
        )