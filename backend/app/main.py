from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.app import route_router, carbon_router, blockchain_router, analytics_router, demo_router
from backend import app
# Include all routers
app.include_router(route_router, prefix="/api/routes", tags=["Route Optimization"])
app.include_router(carbon_router, prefix="/api/carbon", tags=["Carbon Tracking"])
app.include_router(blockchain_router, prefix="/api/blockchain", tags=["Blockchain Verification"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics & Dashboard"])
app.include_router(demo_router, prefix="/api/demo", tags=["Demo Data"])
