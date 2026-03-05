"""
Insights API
Generates sustainability insights from stored ESG metrics.
"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.carbon import CarbonMetric
from app.models.energy import EnergyMetric

logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------
# Insights Endpoint
# ---------------------------------------------------

@router.get("/insights")
def get_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate ESG insights from uploaded sustainability reports.
    """

    # ---------------------------------------------
    # Fetch user documents
    # ---------------------------------------------

    documents = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .all()
    )

    if not documents:
        return {
            "total_documents": 0,
            "unique_companies": 0,
            "reporting_years": [],
            "summary": "No sustainability reports uploaded yet.",
        }

    document_ids = [d.id for d in documents]

    # ---------------------------------------------
    # Company + year stats
    # ---------------------------------------------

    companies = list(
        set(
            doc.company_name
            for doc in documents
            if doc.company_name and doc.company_name != "Unknown"
        )
    )

    reporting_years = list(
        set(
            doc.reporting_year
            for doc in documents
            if doc.reporting_year
        )
    )

    # ---------------------------------------------
    # Carbon emissions insights
    # ---------------------------------------------

    total_scope1 = (
        db.query(func.sum(CarbonMetric.value))
        .filter(CarbonMetric.scope == "scope1_emissions")
        .filter(CarbonMetric.document_id.in_(document_ids))
        .scalar()
    )

    total_scope2 = (
        db.query(func.sum(CarbonMetric.value))
        .filter(CarbonMetric.scope == "scope2_emissions")
        .filter(CarbonMetric.document_id.in_(document_ids))
        .scalar()
    )

    total_scope3 = (
        db.query(func.sum(CarbonMetric.value))
        .filter(CarbonMetric.scope == "scope3_emissions")
        .filter(CarbonMetric.document_id.in_(document_ids))
        .scalar()
    )

    # ---------------------------------------------
    # Energy insights
    # ---------------------------------------------

    avg_renewable_pct = (
        db.query(func.avg(EnergyMetric.value))
        .filter(EnergyMetric.metric_name == "renewable_energy_pct")
        .filter(EnergyMetric.document_id.in_(document_ids))
        .scalar()
    )

    # ---------------------------------------------
    # Generate summary
    # ---------------------------------------------

    summary = (
        f"{len(documents)} sustainability reports were analyzed. "
        f"{len(companies)} companies reported ESG metrics across "
        f"{len(reporting_years)} reporting years. "
    )

    if total_scope1:
        summary += f"Total Scope-1 emissions reported: {round(total_scope1,2)} tCO2e. "

    if avg_renewable_pct:
        summary += f"Average renewable energy usage is {round(avg_renewable_pct,2)}%."

    return {
        "total_documents": len(documents),
        "unique_companies": len(companies),
        "reporting_years": reporting_years,
        "emissions": {
            "scope1_total": total_scope1,
            "scope2_total": total_scope2,
            "scope3_total": total_scope3,
        },
        "energy": {
            "avg_renewable_energy_pct": avg_renewable_pct
        },
        "summary": summary,
    }