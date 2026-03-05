"""
SQLAlchemy Base configuration.

This file imports all models so SQLAlchemy
can register relationships before creating tables.
"""

from app.db.session import Base

# Import models so SQLAlchemy knows about them
from app.models.user import User
from app.models.document import Document
from app.models.carbon import CarbonMetric
from app.models.energy import EnergyMetric
from app.models.water import WaterMetric
from app.models.waste import WasteMetric
