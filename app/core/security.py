from fastapi import Header, HTTPException, status
from app.core.config import API_KEY

async def require_service_key(x_api_key: str = Header(..., alias="x-api-key")) -> str:
    """
    Dependency: require valid x-api-key header. 
    Returns 401 if missing/invalid.
    """
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid API key"
        )
    return x_api_key