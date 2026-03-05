import logging
import pandas as pd
import pdfplumber
import fitz
import pytesseract
from PIL import Image
import io
from pathlib import Path

logger = logging.getLogger(__name__)


class FileParser:

    def parse(self, file_path: str):

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self.parse_pdf(file_path)

        if extension in [".xlsx", ".xls"]:
            return self.parse_excel(file_path)

        raise ValueError("Unsupported file type")

    # ------------------------------------------------
    # PDF PARSER
    # ------------------------------------------------

    def parse_pdf(self, file_path):

        text = []

        try:

            doc = fitz.open(file_path)

            for page in doc:

                page_text = page.get_text()

                if page_text:
                    text.append(page_text)

            doc.close()

        except Exception as e:
            logger.error(f"PDF text extraction failed: {e}")

        try:

            with pdfplumber.open(file_path) as pdf:

                for page in pdf.pages:

                    tables = page.extract_tables()

                    for table in tables:

                        for row in table:

                            cleaned = [
                                str(cell).strip()
                                for cell in row
                                if cell
                            ]

                            if cleaned:
                                text.append(" | ".join(cleaned))

        except Exception as e:
            logger.error(f"Table extraction failed: {e}")

        return "\n".join(text)

    # ------------------------------------------------
    # EXCEL PARSER
    # ------------------------------------------------

    def parse_excel(self, file_path):

        text = []

        try:

            xls = pd.ExcelFile(file_path)

            for sheet in xls.sheet_names:

                df = pd.read_excel(xls, sheet)

                df = df.fillna("")

                text.append(f"Sheet: {sheet}")

                text.append(df.to_string(index=False))

        except Exception as e:
            logger.error(f"Excel parsing error: {e}")

        return "\n".join(text)


parser = FileParser()


def parse_file(file_path):

    return parser.parse(file_path)