"""
Waste metrics model.
Stores waste-related metrics extracted from sustainability reports.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class WasteMetric(Base):
    __tablename__ = "waste_metrics"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    # e.g. "total_generated", "recycling_rate_pct"
    metric_name = Column(String(100), nullable=False)

    value = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)  # e.g. "tonnes", "%"

    document = relationship("Document", back_populates="waste_metrics")
