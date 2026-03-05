from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db, get_current_user
from app.models.document import Document
from app.models.carbon import CarbonMetric
from app.models.energy import EnergyMetric
from app.models.water import WaterMetric
from app.models.waste import WasteMetric
from app.models.user import User


from app.services.esg_insights import generate_insights
from app.services.esg_benchmark import get_company_benchmark

router = APIRouter()


# ---------------------------------------------------------
# BASIC INSIGHTS (existing functionality)
# ---------------------------------------------------------

@router.get("/insights")
def get_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    total_documents = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .count()
    )

    unique_companies = (
        db.query(func.count(func.distinct(Document.company_name)))
        .filter(Document.user_id == current_user.id)
        .scalar()
    )

    reporting_years = (
        db.query(Document.reporting_year)
        .filter(Document.user_id == current_user.id)
        .distinct()
        .all()
    )

    reporting_years = [y[0] for y in reporting_years if y[0] is not None]

    scope1_total = (
        db.query(func.sum(CarbonMetric.value))
        .filter(CarbonMetric.scope == "scope1_emissions")
        .scalar()
    )

    scope2_total = (
        db.query(func.sum(CarbonMetric.value))
        .filter(CarbonMetric.scope == "scope2_emissions")
        .scalar()
    )

    scope3_total = (
        db.query(func.sum(CarbonMetric.value))
        .filter(CarbonMetric.scope == "scope3_emissions")
        .scalar()
    )

    renewable_energy_avg = (
        db.query(func.avg(EnergyMetric.value))
        .filter(EnergyMetric.metric_name == "renewable_energy_pct")
        .scalar()
    )

    summary = (
        f"{total_documents} sustainability reports were analyzed "
        f"across {unique_companies} companies."
    )

    return {
        "total_documents": total_documents,
        "unique_companies": unique_companies,
        "reporting_years": reporting_years,
        "emissions": {
            "scope1_total": scope1_total,
            "scope2_total": scope2_total,
            "scope3_total": scope3_total,
        },
        "energy": {
            "avg_renewable_energy_pct": renewable_energy_avg
        },
        "summary": summary,
    }


# ---------------------------------------------------------
# AI INSIGHTS (NEW ENTERPRISE FEATURE)
# ---------------------------------------------------------

@router.get("/ai-insights")
def ai_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate AI-powered ESG insights
    """

    documents = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .all()
    )

    metrics = []

    for doc in documents:

        scope1 = (
            db.query(func.sum(CarbonMetric.value))
            .filter(CarbonMetric.document_id == doc.id)
            .filter(CarbonMetric.scope == "scope1_emissions")
            .scalar()
        )

        scope2 = (
            db.query(func.sum(CarbonMetric.value))
            .filter(CarbonMetric.document_id == doc.id)
            .filter(CarbonMetric.scope == "scope2_emissions")
            .scalar()
        )

        scope3 = (
            db.query(func.sum(CarbonMetric.value))
            .filter(CarbonMetric.document_id == doc.id)
            .filter(CarbonMetric.scope == "scope3_emissions")
            .scalar()
        )

        renewable = (
            db.query(func.avg(EnergyMetric.value))
            .filter(EnergyMetric.document_id == doc.id)
            .filter(EnergyMetric.metric_name == "renewable_energy_pct")
            .scalar()
        )

        metrics.append({
            "company": doc.company_name,
            "year": doc.reporting_year,
            "scope1": scope1,
            "scope2": scope2,
            "scope3": scope3,
            "renewable_energy_pct": renewable,
        })

    analysis = generate_insights(metrics)

    return {
        "documents_analyzed": len(metrics),
        "analysis": analysis
    }

@router.get("/esg-benchmark")
def esg_benchmark(db: Session = Depends(get_db)):

    results = get_company_benchmark(db)

    return {
        "companies": results,
        "count": len(results)
    }