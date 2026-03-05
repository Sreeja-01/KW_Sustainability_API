"""
Water metrics model.
Stores water-related metrics extracted from sustainability reports.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class WaterMetric(Base):
    __tablename__ = "water_metrics"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    # e.g. "total_withdrawal", "total_consumption"
    metric_name = Column(String(100), nullable=False)

    value = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)  # e.g. "m3"

    document = relationship("Document", back_populates="water_metrics")
