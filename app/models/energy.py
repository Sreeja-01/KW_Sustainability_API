"""
Energy metrics model.
Stores energy-related metrics extracted from sustainability reports.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class EnergyMetric(Base):
    __tablename__ = "energy_metrics"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    # e.g. "total_energy", "renewable_energy_pct"
    metric_name = Column(String(100), nullable=False)

    # numeric value (MWh, %, etc.)
    value = Column(Float, nullable=True)

    # unit for the metric, e.g. "MWh", "%"
    unit = Column(String(50), nullable=True)

    # back-reference to Document
    document = relationship("Document", back_populates="energy_metrics")
