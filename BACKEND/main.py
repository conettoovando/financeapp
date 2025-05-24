from fastapi import FastAPI
from routes.users_routes import router as users_routes
from routes.api_routes import api_router
from database.finance import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Finanzas")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users_routes)
app.include_router(router=api_router, prefix="/api")