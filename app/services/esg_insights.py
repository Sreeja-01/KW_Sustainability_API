import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_insights(metrics):

    try:

        # Handle metrics format
        if isinstance(metrics, list):
            metrics_text = str(metrics[:10])
        else:
            metrics_text = str(metrics)

        prompt = f"""
Analyze ESG sustainability metrics.

Metrics:
{metrics_text}

Provide:

1. Carbon emissions analysis
2. Energy sustainability insights
3. Water and waste observations
4. Overall ESG summary
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[
                {"role": "system", "content": "You are an ESG sustainability analyst."},
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content

    except Exception as e:

        logger.error(f"AI insights failed: {e}")

        return "AI insights unavailable due to API rate limits or temporary error."