import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.database import db_manager
from backend.app.seed.seed_data import seed_database

# Routers
from backend.app.routers.auth import router as auth_router
from backend.app.routers.applications import router as apps_router
from backend.app.routers.documents import router as docs_router
from backend.app.routers.verification import router as verify_router
from backend.app.routers.review import router as review_router
from backend.app.routers.compliance import router as comp_router
from backend.app.routers.reports import router as reports_router
from backend.app.routers.analytics import router as analytics_router
from backend.app.routers.issuers import router as issuers_router
from backend.app.routers.audit import router as audit_router
from backend.app.routers.scenarios import router as scenarios_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to DB and seed demonstration scenarios
    await db_manager.connect()
    try:
        await seed_database()
    except Exception as e:
        print(f"Seed note: {e}")
    yield
    # Shutdown

app = FastAPI(
    title="VERITRUST AI API",
    description="AI-Powered Application Validation, Document Authentication and Regulatory Compliance Verification Platform (SIH26261 | AICTE | Smart Automation)",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(apps_router)
app.include_router(docs_router)
app.include_router(verify_router)
app.include_router(review_router)
app.include_router(comp_router)
app.include_router(reports_router)
app.include_router(analytics_router)
app.include_router(issuers_router)
app.include_router(audit_router)
app.include_router(scenarios_router)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "platform": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database_mode": "MongoDB Atlas" if db_manager.is_atlas else "Local Document Store (Resilient Fallback)",
        "storage": settings.STORAGE_TYPE,
        "timestamp": os.environ.get("CURRENT_TIME", "")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
