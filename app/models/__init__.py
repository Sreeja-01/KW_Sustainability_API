# Import all models so SQLAlchemy can register relationships

from app.models.user import User
from app.models.document import Document
from app.models.carbon import CarbonMetric

# Later we will add
# from app.models.energy import EnergyMetric
# from app.models.water import WaterMetric
# from app.models.waste import WasteMetric