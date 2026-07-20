from fastapi import FastAPI

from app.database.database import engine
from app.properties import models
from app.properties.routes import router as property_router
from app.customers.router import router as customer_router
from app.leads.router import router as lead_router
from fastapi import FastAPI, Depends
from app.core.config import Settings, get_settings
from app.core.middleware import LoggingMiddleware
from app.core.handlers import register_exception_handlers
from app.benchmark.router import router as benchmark_router
from app.users.router import router as user_router
from app.leads.websocket import router as websocket_router
import asyncio
from app.webhooks.router import router as webhook_router

from app.core.websocket import manager

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    manager.set_loop(
        asyncio.get_running_loop()
    )
    
    
app.include_router(webhook_router)


app.add_middleware(LoggingMiddleware)
register_exception_handlers(app)
app.include_router(benchmark_router)
app.include_router(user_router)
app.include_router(websocket_router)


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