from fastapi import FastAPI

from app.database.database import engine
from app.properties import models
from app.properties.routes import router as property_router
from app.customers.router import router as customer_router
from app.leads.router import router as lead_router
from fastapi import FastAPI, Depends
from app.core.config import Settings, get_settings


app = FastAPI()


app.include_router(property_router)
app.include_router(customer_router)
app.include_router(lead_router)


@app.get("/")
def home(
    settings: Settings = Depends(get_settings)
):
    return {
        "message": "Real Estate API is running",
        "docs_enabled": settings.enable_docs
    }