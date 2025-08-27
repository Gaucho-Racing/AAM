from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from loguru import logger

from aam.service.iam import ADMIN_ROLE_ARN, MEMBER_ROLE_ARN, IAMService
from aam.service.sentinel import Sentinel

router = APIRouter()


@router.post("/iam/login")
async def login(request: Request):
    if not request.headers.get("Authorization"):
        return JSONResponse(
            status_code=401,
            content={"message": "you are not authorized to access this resource"},
        )

    try:
        access_token = request.headers.get("Authorization").split(" ")[1]
        user = Sentinel.get_current_user(access_token)
        if user.is_inner_circle():
            logger.info(
                f"User {user.id} is an inner circle member, assuming admin role"
            )
            creds = IAMService.assume_role(
                access_token, ADMIN_ROLE_ARN, session_name=user.email
            )
        else:
            logger.info(
                f"User {user.id} is not an inner circle member, assuming member role"
            )
            creds = IAMService.assume_role(
                access_token, MEMBER_ROLE_ARN, session_name=user.email
            )
        url = IAMService.build_console_login_url(creds)
        creds["login_url"] = url
        return creds
    except Exception as e:
        logger.error(f"Error building login URL: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": str(e)},
        )
