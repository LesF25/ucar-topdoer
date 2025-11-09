from fastapi import APIRouter

from .incidents import router as incident_router

api_router = APIRouter(prefix='/api')
api_router.include_router(incident_router)
