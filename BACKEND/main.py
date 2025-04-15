from fastapi import FastAPI
from routes import user_routes
from database.user import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Finanzas")

app.include_router(user_routes.router)