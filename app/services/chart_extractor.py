import cv2
import pytesseract
import fitz
import numpy as np
from PIL import Image
import io


def extract_chart_numbers(pdf_path):

    doc = fitz.open(pdf_path)

    numbers = []

    for page in doc:

        images = page.get_images(full=True)

        for img in images:

            xref = img[0]
            base = doc.extract_image(xref)

            image_bytes = base["image"]

            image = Image.open(io.BytesIO(image_bytes))

            text = pytesseract.image_to_string(image)

            numbers += [int(x) for x in text.split() if x.isdigit()]

    return numbers