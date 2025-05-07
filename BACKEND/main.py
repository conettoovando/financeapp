from fastapi import FastAPI
from routes import users_routes, cuenta_routes
from database.finance import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Finanzas")

app.include_router(users_routes.router)
app.include_router(router=cuenta_routes.router, prefix="/api")