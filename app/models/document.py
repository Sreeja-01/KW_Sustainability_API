"""
Document model.

Represents uploaded sustainability reports and extracted ESG metadata.
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    BigInteger,
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class Document(Base):
    __tablename__ = "documents"

    # -----------------------------
    # Primary Key
    # -----------------------------
    id = Column(Integer, primary_key=True, index=True)

    # -----------------------------
    # File Information
    # -----------------------------
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    mime_type = Column(String, nullable=True)
    file_size = Column(BigInteger, nullable=True)

    # -----------------------------
    # Extracted Metadata
    # -----------------------------
    company_name = Column(String, index=True)
    reporting_year = Column(Integer, index=True)
    status = Column(String, default="pending")

    # -----------------------------
    # Ownership
    # -----------------------------
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="documents")

    # -----------------------------
    # Processing timestamps
    # -----------------------------
    processed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # -----------------------------
    # ESG Metric Relationships
    # -----------------------------
    carbon_metrics = relationship(
        "CarbonMetric",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    energy_metrics = relationship(
        "EnergyMetric",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    water_metrics = relationship(
        "WaterMetric",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    waste_metrics = relationship(
        "WasteMetric",
        back_populates="document",
        cascade="all, delete-orphan",
    )
