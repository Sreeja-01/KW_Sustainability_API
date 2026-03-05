"""
Semantic search API for ESG reports
"""

from fastapi import APIRouter, Query
from app.services.vector_store import search

router = APIRouter()


@router.get("/search")
def semantic_search(q: str = Query(..., description="Search query")):
    """
    Search ESG reports using semantic vector search
    """

    results = search(q)

    return {
        "query": q,
        "results": results,
        "count": len(results)
    }