"""
Health check endpoints.
"""
from fastapi import APIRouter, Depends

from db.neo4j import get_neo4j_driver
from db.qdrant import get_qdrant_client
from models.schemas import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check():
    """
    Check if the API is running.
    """
    return HealthResponse(status="ok", version="0.1.0")


@router.get("/db", response_model=HealthResponse)
async def db_health_check(
    qdrant=Depends(get_qdrant_client),
    neo4j=Depends(get_neo4j_driver)
):
    """
    Check if the databases are connected.
    """
    status = "ok"
    message = "All databases connected"
    
    try:
        # Check Qdrant connection
        qdrant.get_collections()
        
        # Check Neo4j connection
        with neo4j.session() as session:
            session.run("RETURN 1")
    except Exception as e:
        status = "error"
        message = f"Database error: {str(e)}"
    
    return HealthResponse(status=status, message=message)
