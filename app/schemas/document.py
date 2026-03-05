"""
Pydantic schemas for Document API responses.
"""

from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


# ------------------------------
# Document Response
# ------------------------------

class DocumentResponse(BaseModel):

    id: int
    filename: str
    company_name: Optional[str] = None
    reporting_year: Optional[int] = None
    status: Optional[str] = None

    file_path: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None

    user_id: Optional[int] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ------------------------------
# Pagination Response
# ------------------------------

class DocumentsListResponse(BaseModel):

    total: int
    limit: int
    skip: int
    data: List[DocumentResponse]


# ------------------------------
# Insights Response
# ------------------------------

class InsightsResponse(BaseModel):

    total_documents: int
    companies: int
    latest_reports: List[DocumentResponse]