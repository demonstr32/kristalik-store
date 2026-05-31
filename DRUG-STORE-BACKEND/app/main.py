from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.auth import router as auth_router
from app.api.routers.prod import router as prod_router

app = FastAPI(title="Drug Store API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(prod_router)

@app.get("/")
def root():
    return {"message": "Drug Store API is running"}