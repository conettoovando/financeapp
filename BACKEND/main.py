from fastapi import FastAPI
from routes.users_routes import router as users_routes
from routes.api_routes import api_router
from database.finance import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Finanzas")

app.include_router(users_routes)
app.include_router(router=api_router, prefix="/api")