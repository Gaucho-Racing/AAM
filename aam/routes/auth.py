from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from aam.service.sentinel import Sentinel, SentinelError

router = APIRouter()


@router.post("/auth/login")
async def login(code: str = Query(..., description="OAuth authorization code")):
    try:
        token = Sentinel.exchange_code_for_token(code)
        return token
    except SentinelError as e:
        # Return the original API error status code with "message" key
        return JSONResponse(status_code=e.code, content={"message": e.message})
    except Exception as e:
        # Handle unexpected errors with "message" key
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/auth/refresh")
async def refresh(token: str = Query(..., description="Refresh token")):
    try:
        token = Sentinel.refresh_credentials(token)
        return token
    except SentinelError as e:
        # Return the original API error status code with "message" key
        return JSONResponse(status_code=e.code, content={"message": e.message})
    except Exception as e:
        # Handle unexpected errors with "message" key
        return JSONResponse(status_code=500, content={"message": str(e)})
