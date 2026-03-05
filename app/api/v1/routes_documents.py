"""
Document API routes
"""

import os
import uuid
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.document import Document
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


# ---------------------------------------------------
# Upload Document
# ---------------------------------------------------

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
                detail="File exceeds maximum allowed size",
            )

        unique_filename = f"{uuid.uuid4()}_{file.filename}"

        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as f:
            f.write(contents)

        logger.info(f"File uploaded {unique_filename}")

        # -------------------------------
        # Parse document text
        # -------------------------------

        text = parse_file(file_path)
        from app.services.vector_store import add_document

        add_document(text, {"filename": file.filename})

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from file",
            )

        # -------------------------------
        # ESG extraction
        # -------------------------------

        extractor = get_extractor()

        metrics = extractor(text) or {}

        # -------------------------------
        # Safe values
        # -------------------------------

        company_name = metrics.get("company_name", "Unknown")
        reporting_year: Optional[int] = metrics.get("reporting_year")

        carbon = metrics.get("carbon", {})
        energy = metrics.get("energy", {})
        water = metrics.get("water", {})
        waste = metrics.get("waste", {})

        # -------------------------------
        # Save document
        # -------------------------------

        document = Document(
            filename=unique_filename,
            company_name=company_name,
            reporting_year=reporting_year,
            status="processed",
            user_id=current_user.id,
            file_path=file_path,
            file_size=len(contents),
            mime_type=file.content_type,
            processed_at=datetime.utcnow(),
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        # -------------------------------
        # Save carbon metrics
        # -------------------------------

        for scope, value in carbon.items():

            db.add(
                CarbonMetric(
                    document_id=document.id,
                    scope=scope,
                    value=value,
                    unit="tCO2e",
                )
            )

        # -------------------------------
        # Save energy metrics
        # -------------------------------

        for name, value in energy.items():

            db.add(
                EnergyMetric(
                    document_id=document.id,
                    metric_name=name,
                    value=value,
                    unit=None,
                )
            )

        # -------------------------------
        # Save water metrics
        # -------------------------------

        for name, value in water.items():

            db.add(
                WaterMetric(
                    document_id=document.id,
                    metric_name=name,
                    value=value,
                    unit="m3",
                )
            )

        # -------------------------------
        # Save waste metrics
        # -------------------------------

        for name, value in waste.items():

            db.add(
                WasteMetric(
                    document_id=document.id,
                    metric_name=name,
                    value=value,
                    unit=None,
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

        logger.exception("Upload failed")

        raise HTTPException(
            status_code=500,
            detail="Document processing failed",
        )


# ---------------------------------------------------
# List Documents
# ---------------------------------------------------

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
        query = query.filter(
            Document.company_name.ilike(f"%{company_name}%")
        )

    total = query.count()

    docs = query.offset(skip).limit(limit).all()

    page = (skip // limit) + 1

    data = []

    for doc in docs:

        data.append(
            {
                "id": doc.id,
                "filename": doc.filename,
                "company_name": doc.company_name,
                "reporting_year": doc.reporting_year,
                "status": doc.status,
                "created_at": doc.created_at,
            }
        )

    return {
        "total": total,
        "page": page,
        "page_size": limit,
        "has_next": total > skip + limit,
        "data": data,
    }


# ---------------------------------------------------
# Document Detail
# ---------------------------------------------------

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
        "carbon_metrics": [
            {"scope": m.scope, "value": m.value, "unit": m.unit}
            for m in document.carbon_metrics
        ],
        "energy_metrics": [
            {"metric_name": m.metric_name, "value": m.value, "unit": m.unit}
            for m in document.energy_metrics
        ],
        "water_metrics": [
            {"metric_name": m.metric_name, "value": m.value, "unit": m.unit}
            for m in document.water_metrics
        ],
        "waste_metrics": [
            {"metric_name": m.metric_name, "value": m.value, "unit": m.unit}
            for m in document.waste_metrics
        ],
    }