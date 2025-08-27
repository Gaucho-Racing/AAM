from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from aam.service.sentinel import Sentinel, SentinelError

router = APIRouter()


@router.get("/users")
async def get_all_users():
    try:
        users = Sentinel.get_all_users()
        return users
    except SentinelError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/users/@me")
async def get_current_user(request: Request):
    if not request.headers.get("Authorization"):
        return JSONResponse(
            status_code=401,
            content={"message": "you are not authorized to access this resource"},
        )

    try:
        access_token = request.headers.get("Authorization").split(" ")[1]
        user = Sentinel.get_current_user(access_token)
        return user
    except SentinelError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        user = Sentinel.get_user(user_id)
        return user
    except SentinelError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
