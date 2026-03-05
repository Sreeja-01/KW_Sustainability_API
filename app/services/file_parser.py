"""
File parser service.

Supports:
- PDF parsing
- Excel parsing

Returns extracted text for LLM processing.
"""

import logging
import pandas as pd
from pathlib import Path

from pdfminer.high_level import extract_text

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# PDF Parsing
# ---------------------------------------------------------

def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """

    try:
        text = extract_text(file_path)

        if not text:
            logger.warning("No text extracted from PDF")

        return text

    except Exception as e:
        logger.error(f"PDF parsing failed: {e}")
        return ""


# ---------------------------------------------------------
# Excel Parsing (IMPROVED)
# ---------------------------------------------------------

def parse_excel(file_path: str) -> str:
    """
    Extract structured text from Excel file
    so the LLM can understand sustainability metrics.
    """

    try:

        text_parts = []

        xls = pd.ExcelFile(file_path)

        for sheet_name in xls.sheet_names:

            df = pd.read_excel(xls, sheet_name)

            text_parts.append(f"\nSheet: {sheet_name}\n")

            # convert each row to readable sentence
            for _, row in df.iterrows():

                row_parts = []

                for column, value in row.items():

                    if pd.notna(value):

                        row_parts.append(f"{column}: {value}")

                if row_parts:

                    sentence = " | ".join(row_parts)

                    text_parts.append(sentence)

        return "\n".join(text_parts)

    except Exception as e:
        logger.error(f"Excel parsing failed: {e}")
        return ""


# ---------------------------------------------------------
# File Type Detection
# ---------------------------------------------------------

def parse_file(file_path: str) -> str:
    """
    Detect file type and parse accordingly.
    """

    path = Path(file_path)

    suffix = path.suffix.lower()

    if suffix == ".pdf":

        return parse_pdf(file_path)

    elif suffix in [".xlsx", ".xls"]:

        return parse_excel(file_path)

    else:

        logger.error(f"Unsupported file type: {suffix}")

        return ""