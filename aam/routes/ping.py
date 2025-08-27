from fastapi import APIRouter

from aam.config.config import Config

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"message": f"AAM v{Config.VERSION} is online!"}
