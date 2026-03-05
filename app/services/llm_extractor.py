import os
import re
import json
import logging
from typing import Dict

from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def normalize_number(value):

    if value is None:
        return None

    try:
        value = str(value)
        value = value.replace(",", "")
        value = value.replace("%", "")

        return float(value)

    except Exception:
        return None


# ---------------------------------------------------
# COMPANY + YEAR EXTRACTION
# ---------------------------------------------------

def extract_company(text):

    patterns = [
        r"(.*?)\s+Environmental Sustainability Report",
        r"(.*?)\s+Sustainability Report",
        r"(.*?)\s+Environmental Report",
        r"(.*?)\s+ESG Report",
    ]

    for pattern in patterns:

        match = re.search(pattern, text[:3000], re.IGNORECASE)

        if match:

            name = match.group(1).strip()

            if len(name) < 120:
                name = name.replace("|", "").strip()
                name = name.replace("2024", "").strip()
                return name

    return None


def extract_year(text):

    match = re.search(r"(20[1-3][0-9])", text[:2000])

    if match:
        return int(match.group(1))

    return None


# ---------------------------------------------------
# REGEX EXTRACTION
# ---------------------------------------------------

def extract_with_regex(text):

    text_lower = text.lower()

    metrics = {
        "company_name": None,
        "reporting_year": None,
        "carbon": {},
        "energy": {},
        "water": {},
        "waste": {}
    }

    patterns = {

        "scope1_emissions": r"scope\s*1[^0-9]{0,30}([0-9,\.]+)",
        "scope2_emissions": r"scope\s*2[^0-9]{0,30}([0-9,\.]+)",
        "scope3_emissions": r"scope\s*3[^0-9]{0,30}([0-9,\.]+)",

        "renewable_energy_pct": r"([0-9]+\.?[0-9]*)\s*%\s*renewable",

        "water_withdrawal": r"water[^0-9]{0,20}([0-9,\.]+)\s*(m3|million)",
        "waste_generated": r"waste[^0-9]{0,20}([0-9,\.]+)\s*(tons|tonnes)"
    }

    for key, pattern in patterns.items():

        match = re.search(pattern, text_lower)

        if match:

            value = normalize_number(match.group(1))

            if "scope" in key:

                metrics["carbon"][key] = value

            elif "renewable" in key:

                metrics["energy"]["renewable_energy_pct"] = value

            elif "water" in key:

                metrics["water"]["total_withdrawal"] = value

            elif "waste" in key:

                metrics["waste"]["total_generated"] = value

    return metrics


# ---------------------------------------------------
# LLM EXTRACTION
# ---------------------------------------------------

def extract_with_llm(text):

    prompt = f"""
Extract ESG sustainability metrics.

Return VALID JSON only.

Format:

{{
"company_name": "...",
"reporting_year": 2024,
"carbon": {{
"scope1_emissions": number,
"scope2_emissions": number,
"scope3_emissions": number
}},
"energy": {{
"total_energy": number,
"renewable_energy_pct": number
}},
"water": {{
"total_withdrawal": number
}},
"waste": {{
"total_generated": number
}}
}}

TEXT:
{text[:8000]}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[
                {"role": "system", "content": "You extract ESG metrics."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content

        json_match = re.search(r"\{.*\}", content, re.S)

        if json_match:
            return json.loads(json_match.group())

    except Exception as e:

        logger.error(f"LLM extraction failed: {e}")

    return {}


# ---------------------------------------------------
# MERGE DATA
# ---------------------------------------------------

def merge_metrics(regex_data, llm_data, company, year):

    result = regex_data

    if company:
        result["company_name"] = company

    if year:
        result["reporting_year"] = year

    for category in ["carbon", "energy", "water", "waste"]:

        if category in llm_data:

            for key, value in llm_data[category].items():

                if value and key not in result[category]:

                    result[category][key] = normalize_number(value)

    return result


# ---------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------

def extract_esg_metrics(text: str):

    company = extract_company(text)
    year = extract_year(text)

    regex_metrics = extract_with_regex(text)

    llm_metrics = extract_with_llm(text)

    final_metrics = merge_metrics(regex_metrics, llm_metrics, company, year)

    return final_metrics


def get_extractor():
    return extract_esg_metrics