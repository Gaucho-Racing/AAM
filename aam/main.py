import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aam.config.config import Config
from aam.routes import auth, iam, ping, user
from aam.service.auth import AuthService
from aam.service.sentinel import Sentinel


def create_app():
    app = FastAPI(
        title="Gaucho Racing AAM",
        description="API Documentation",
        version=Config.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ping.router, tags=["Ping"])
    app.include_router(auth.router, tags=["Auth"])
    app.include_router(user.router, tags=["User"])
    app.include_router(iam.router, tags=["IAM"])

    return app


def main():
    AuthService.configure(
        jwks_url=Config.SENTINEL_JWKS_URL,
        issuer="https://sso.gauchoracing.com",
        audience=Config.SENTINEL_CLIENT_ID,
    )
    if not Sentinel.ping():
        raise Exception("Can't reach Sentinel API!")

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT)


if __name__ == "__main__":
    main()
