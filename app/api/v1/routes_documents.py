"""
Document API routes

Handles:
- Upload sustainability reports (PDF / Excel)
- Parse files
- Extract ESG metrics with LLM
- Store results in database
- List documents with pagination
- Get document details
"""

import os
import logging
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.document import Document
from app.models.user import User
from app.models.carbon import CarbonMetric
from app.models.energy import EnergyMetric
from app.models.water import WaterMetric
from app.models.waste import WasteMetric
from app.services.file_parser import parse_file
from app.services.llm_extractor import get_extractor
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_DIR = settings.UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------------------------------------------
# Upload Document
# ---------------------------------------------------------

@router.post("/upload", status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:

        allowed_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
        ]

        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and Excel files are supported",
            )

        contents = await file.read()

        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File too large. Max allowed size is 50MB",
            )

        existing_doc = (
            db.query(Document)
            .filter(Document.user_id == current_user.id)
            .filter(Document.filename == file.filename)
            .filter(Document.file_size == len(contents))
            .first()
        )

        if existing_doc:
            raise HTTPException(
                status_code=409,
                detail="This document has already been uploaded",
            )

        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        logger.info(f"File uploaded: {unique_filename}")

        try:
            text = parse_file(file_path)
        except Exception as e:
            logger.error(f"File parsing failed: {e}")
            raise HTTPException(status_code=400, detail="File parsing failed")

        if not text or len(text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from document",
            )

        extractor = get_extractor()

        try:
            metrics = extractor.extract_metrics(text)
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            metrics = None

        company_name = "Unknown"
        reporting_year: Optional[int] = None

        if metrics:
            company_name = metrics.company_name or "Unknown"
            reporting_year = metrics.reporting_year

        document = Document(
            filename=unique_filename,  # store actual saved filename
            company_name=company_name,
            reporting_year=reporting_year,
            status="processed" if metrics else "pending",
            user_id=current_user.id,
            file_path=file_path,
            file_size=len(contents),
            mime_type=file.content_type,
            processed_at=datetime.utcnow(),
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        if metrics:

            for scope_name, payload in (metrics.carbon_metrics or {}).items():

                value = None
                unit = None

                if isinstance(payload, dict):
                    value = payload.get("value")
                    unit = payload.get("unit")
                else:
                    value = payload

                db.add(
                    CarbonMetric(
                        document_id=document.id,
                        scope=scope_name,
                        value=value,
                        unit=unit or "tCO2e",
                    )
                )

            for metric_name, payload in (metrics.energy_metrics or {}).items():

                value = None
                unit = None

                if isinstance(payload, dict):
                    value = payload.get("value")
                    unit = payload.get("unit")
                else:
                    value = payload

                db.add(
                    EnergyMetric(
                        document_id=document.id,
                        metric_name=metric_name,
                        value=value,
                        unit=unit,
                    )
                )

            for metric_name, payload in (metrics.water_metrics or {}).items():

                value = None
                unit = None

                if isinstance(payload, dict):
                    value = payload.get("value")
                    unit = payload.get("unit")
                else:
                    value = payload

                db.add(
                    WaterMetric(
                        document_id=document.id,
                        metric_name=metric_name,
                        value=value,
                        unit=unit,
                    )
                )

            for metric_name, payload in (metrics.waste_metrics or {}).items():

                value = None
                unit = None

                if isinstance(payload, dict):
                    value = payload.get("value")
                    unit = payload.get("unit")
                else:
                    value = payload

                db.add(
                    WasteMetric(
                        document_id=document.id,
                        metric_name=metric_name,
                        value=value,
                        unit=unit,
                    )
                )

            db.commit()

        return {
            "id": document.id,
            "filename": document.filename,
            "company_name": document.company_name,
            "reporting_year": document.reporting_year,
            "status": document.status,
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(f"Upload error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Document processing failed",
        )


# ---------------------------------------------------------
# List Documents (Improved Pagination)
# ---------------------------------------------------------

@router.get("/documents")
def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    company_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    query = db.query(Document).filter(Document.user_id == current_user.id)

    if company_name:
        query = query.filter(Document.company_name.ilike(f"%{company_name}%"))

    total = query.count()

    documents = query.offset(skip).limit(limit).all()

    page = (skip // limit) + 1

    data = [
        {
            "id": doc.id,
            "filename": doc.filename,
            "company_name": doc.company_name,
            "reporting_year": doc.reporting_year,
            "status": doc.status,
            "created_at": doc.created_at,
        }
        for doc in documents
    ]

    return {
        "total": total,
        "page": page,
        "page_size": limit,
        "has_next": total > skip + limit,
        "data": data,
    }


# ---------------------------------------------------------
# Get Document Detail
# ---------------------------------------------------------

@router.get("/documents/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .filter(Document.user_id == current_user.id)
        .first()
    )

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    carbon_metrics = [
        {"scope": m.scope, "value": m.value, "unit": m.unit}
        for m in document.carbon_metrics
    ]

    energy_metrics = [
        {"metric_name": m.metric_name, "value": m.value, "unit": m.unit}
        for m in document.energy_metrics
    ]

    water_metrics = [
        {"metric_name": m.metric_name, "value": m.value, "unit": m.unit}
        for m in document.water_metrics
    ]

    waste_metrics = [
        {"metric_name": m.metric_name, "value": m.value, "unit": m.unit}
        for m in document.waste_metrics
    ]

    return {
        "id": document.id,
        "filename": document.filename,
        "company_name": document.company_name,
        "reporting_year": document.reporting_year,
        "status": document.status,
        "file_size": document.file_size,
        "mime_type": document.mime_type,
        "file_path": document.file_path,
        "processed_at": document.processed_at,
        "created_at": document.created_at,
        "updated_at": document.updated_at,
        "carbon_metrics": carbon_metrics,
        "energy_metrics": energy_metrics,
        "water_metrics": water_metrics,
        "waste_metrics": waste_metrics,
    }