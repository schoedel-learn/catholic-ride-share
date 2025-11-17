"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import auth, users, rides, drivers, parishes
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Catholic Ride Share - Connecting faithful community members for transportation to Mass, Confession, and Church events",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(rides.router, prefix=f"{settings.API_V1_STR}/rides", tags=["rides"])
app.include_router(drivers.router, prefix=f"{settings.API_V1_STR}/drivers", tags=["drivers"])
app.include_router(parishes.router, prefix=f"{settings.API_V1_STR}/parishes", tags=["parishes"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Catholic Ride Share API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
