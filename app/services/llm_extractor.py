"""
LLM extraction service using Groq.
Production-ready ESG sustainability extractor.

Features
- Handles large documents (chunking)
- ESG keyword filtering
- JSON-only responses
- Metrics merging across chunks
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from groq import Groq

from app.core.config import settings  # load GROQ_API_KEY from your Settings

logger = logging.getLogger(__name__)


# =========================
# Data Structure
# =========================


@dataclass
class SustainabilityMetrics:
    company_name: Optional[str] = None
    reporting_year: Optional[int] = None
    carbon_metrics: Dict[str, Any] = field(default_factory=dict)
    energy_metrics: Dict[str, Any] = field(default_factory=dict)
    water_metrics: Dict[str, Any] = field(default_factory=dict)
    waste_metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "company_name": self.company_name,
            "reporting_year": self.reporting_year,
            "carbon_metrics": self.carbon_metrics,
            "energy_metrics": self.energy_metrics,
            "water_metrics": self.water_metrics,
            "waste_metrics": self.waste_metrics,
        }


# =========================
# ESG Keyword Filter
# =========================


def filter_esg_text(text: str) -> str:
    """
    Filter text to keep only ESG-related lines.
    Improves LLM accuracy and reduces token usage.
    """
    ESG_KEYWORDS = [
        "emissions",
        "scope 1",
        "scope 2",
        "scope 3",
        "carbon",
        "co2",
        "ghg",
        "mtco2e",
        "energy",
        "renewable",
        "electricity",
        "mwh",
        "water",
        "withdrawal",
        "consumption",
        "m3",
        "waste",
        "recycling",
        "tonnes",
        "metric tons",
        "sustainability",
        "environment",
    ]

    filtered_lines: List[str] = []
    for line in text.split("\n"):
        lower = line.lower()
        if any(keyword in lower for keyword in ESG_KEYWORDS):
            filtered_lines.append(line)

    joined = "\n".join(filtered_lines)
    # soft length cap so chunks stay reasonable
    return joined[:20000]


# =========================
# LLM Prompt
# =========================


class LLMPrompts:
    @staticmethod
    def extraction_prompt(text: str) -> str:
        """
        Prompt instructing the model to output JSON only in a fixed schema,
        and to use ONLY numbers that actually appear in the document text.
        """
        return f"""
You are an ESG sustainability data extraction AI.

Task:
- Read the sustainability report text.
- Identify the most recent reporting year (for example: 2024 / FY24).
- Extract ONLY numeric values that are explicitly present in the text.
- Map them into the JSON schema below.

Important:
- Use a value ONLY if the number and its unit appear clearly in the text.
  Examples of valid patterns:
    - "92 tCO2e"
    - "149,000 tCO2e"
    - "121 tonnes of waste"
    - "34 GW of renewable energy"
    - "114,000 metric tons of waste diverted"
- If you do NOT see a clear numeric value for a field, leave its "value" as null.
- Do not guess or fabricate numbers.

Return ONLY valid JSON in this exact format (keys must match):

{{
  "company_name": "",
  "reporting_year": null,
  "carbon_metrics": {{
    "scope1_emissions": {{"value": null, "unit": "tCO2e"}},
    "scope2_emissions": {{"value": null, "unit": "tCO2e"}},
    "scope3_emissions": {{"value": null, "unit": "tCO2e"}},
    "total_emissions": {{"value": null, "unit": "tCO2e"}}
  }},
  "energy_metrics": {{
    "total_energy": {{"value": null, "unit": "MWh"}},
    "renewable_energy_pct": null
  }},
  "water_metrics": {{
    "total_withdrawal": {{"value": null, "unit": "m3"}},
    "total_consumption": {{"value": null, "unit": "m3"}}
  }},
  "waste_metrics": {{
    "total_generated": {{"value": null, "unit": "tonnes"}},
    "recycling_rate_pct": null
  }}
}}

Rules:
- Use ONLY numbers that appear in the text with appropriate units.
- If a metric is only described qualitatively or as a percentage change
  (for example "increased by 26% from 2020 baseline") but you do NOT see
  an absolute tCO2e number, leave "value" as null.
- Do NOT add extra top-level keys.
- Do NOT output explanations, comments, or markdown. Output JSON only.

Document text:
{text}
""".strip()


# =========================
# Helper Functions
# =========================


def clean_json(content: str) -> Optional[Dict[str, Any]]:
    """
    Robust JSON cleaner.
    Supports:
    - Raw JSON
    - JSON wrapped in ```json ... ```
    - Extra text before/after
    """
    if not content:
        return None

    try:
        return json.loads(content)
    except Exception:
        cleaned = (
            content.replace("```json", "")
            .replace("```", "")
            .strip()
        )
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1:
            return None
        try:
            return json.loads(cleaned[start : end + 1])
        except Exception as e:
            logger.error(f"JSON parse failed: {e}")
            return None


def split_text(text: str, chunk_size: int = 3000) -> List[str]:
    """
    Split large document text into manageable chunks.
    """
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


# =========================
# Main Extractor
# =========================


class GroqExtractor:
    def __init__(self) -> None:
        # Load key from your Pydantic Settings (which reads .env)
        api_key = settings.GROQ_API_KEY

        if not api_key:
            logger.error("GROQ_API_KEY not set in settings; LLM extraction disabled.")
            self.client = None
            self.model = None
            self.max_chunks = 0
            return

        self.client = Groq(api_key=api_key)
        # You can also use settings.LLM_MODEL if you like
        self.model = "llama-3.3-70b-versatile"
        self.max_chunks = 8

        logger.info("Groq LLM extractor initialized successfully")

    def call_llm(self, prompt: str) -> Optional[Dict[str, Any]]:
        if not self.client:
            logger.warning("LLM client not initialized")
            return None

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Extract ESG sustainability metrics as JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=2000,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                logger.warning("Empty response from LLM")
                return None

            logger.info("LLM response received")
            return clean_json(content)

        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return None

    def merge_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge multiple partial JSON results into one.
        Later chunks can fill nulls from earlier ones.
        """
        merged: Dict[str, Any] = {
            "company_name": None,
            "reporting_year": None,
            "carbon_metrics": {},
            "energy_metrics": {},
            "water_metrics": {},
            "waste_metrics": {},
        }

        for result in results:
            if not merged["company_name"] and result.get("company_name"):
                merged["company_name"] = result["company_name"]

            if not merged["reporting_year"] and result.get("reporting_year"):
                merged["reporting_year"] = result["reporting_year"]

            for metric_group in [
                "carbon_metrics",
                "energy_metrics",
                "water_metrics",
                "waste_metrics",
            ]:
                data = result.get(metric_group)
                if isinstance(data, dict):
                    # later chunks can overwrite earlier nulls or fill missing keys
                    merged[metric_group].update(data)

        return merged

    def extract_metrics(self, doc_text: str) -> Optional[SustainabilityMetrics]:
        if not doc_text:
            logger.warning("Empty document text")
            return None

        try:
            # Filter to ESG-heavy lines first
            filtered_text = filter_esg_text(doc_text)
            if not filtered_text:
                filtered_text = doc_text

            chunks = split_text(filtered_text)
            logger.info(f"Document split into {len(chunks)} chunks")

            results: List[Dict[str, Any]] = []

            for chunk in chunks[: self.max_chunks]:
                prompt = LLMPrompts.extraction_prompt(chunk)
                data = self.call_llm(prompt)
                if data:
                    results.append(data)

            if not results:
                logger.warning("No ESG metrics extracted")
                return None

            merged = self.merge_results(results)

            metrics = SustainabilityMetrics(
                company_name=merged.get("company_name"),
                reporting_year=merged.get("reporting_year"),
                carbon_metrics=merged.get("carbon_metrics", {}),
                energy_metrics=merged.get("energy_metrics", {}),
                water_metrics=merged.get("water_metrics", {}),
                waste_metrics=merged.get("waste_metrics", {}),
            )

            return metrics

        except Exception as e:
            logger.error(f"Extraction pipeline failed: {e}")
            return None


# =========================
# Singleton Instance
# =========================

_extractor: Optional[GroqExtractor] = None


def get_extractor() -> GroqExtractor:
    global _extractor
    if _extractor is None:
        _extractor = GroqExtractor()
    return _extractor
