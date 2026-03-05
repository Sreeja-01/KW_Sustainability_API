"""
Carbon metrics model.

Stores carbon/emissions-related metrics extracted from sustainability reports.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class CarbonMetric(Base):
    __tablename__ = "carbon_metrics"

    id = Column(Integer, primary_key=True, index=True)

    # Link back to document
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    # e.g. "scope1_emissions", "scope2_emissions", "scope3_emissions", "total_emissions"
    scope = Column(String(100), nullable=False)

    # Numeric value of the metric
    value = Column(Float, nullable=True)

    # Unit, default tCO2e
    unit = Column(String(50), default="tCO2e")

    # Relationship back to Document
    document = relationship("Document", back_populates="carbon_metrics")
