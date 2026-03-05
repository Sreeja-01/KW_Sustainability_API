from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.document import Document
from app.models.carbon import CarbonMetric
from app.models.energy import EnergyMetric


def calculate_esg_score(scope1, scope2, renewable):

    score = 50

    if renewable:
        score += min(renewable / 2, 30)

    if scope1:
        score -= min(scope1 / 1000, 10)

    if scope2:
        score -= min(scope2 / 1000, 10)

    return round(score)


def get_company_benchmark(db: Session):

    companies = db.query(Document.company_name)\
        .filter(Document.company_name != None)\
        .distinct().all()

    results = []

    for (company,) in companies:

        scope1 = db.query(func.sum(CarbonMetric.value))\
            .join(Document)\
            .filter(Document.company_name == company)\
            .filter(CarbonMetric.scope == "scope1_emissions")\
            .scalar()

        scope2 = db.query(func.sum(CarbonMetric.value))\
            .join(Document)\
            .filter(Document.company_name == company)\
            .filter(CarbonMetric.scope == "scope2_emissions")\
            .scalar()

        renewable = db.query(func.avg(EnergyMetric.value))\
            .join(Document)\
            .filter(Document.company_name == company)\
            .filter(EnergyMetric.metric_name == "renewable_energy_pct")\
            .scalar()

        score = calculate_esg_score(scope1 or 0, scope2 or 0, renewable or 0)

        results.append({
            "company": company,
            "esg_score": score,
            "renewable_energy": renewable,
            "scope1_emissions": scope1,
            "scope2_emissions": scope2
        })

    results = sorted(results, key=lambda x: x["esg_score"], reverse=True)

    return results