from fastapi import FastAPI
from auth.routers.auth_routes import api_router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from auth.database.db_models.auth_orm import database

def get_app():
    app = FastAPI(
        title="KTutors Authentication Routes",
        description=(
            "This routes here authenticate requests "
            "for all other services of KTutors Project\t"
            "As well as perform all necessary authentation services"
        ),
        version="0.0.1",
    )

    app.include_router(auth_router)

    @app.on_event("startup")
    async def startup():
        await database.connect()
        print("db connected")
        #! save_private_key()

        
    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()
        print("db disconnected")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
