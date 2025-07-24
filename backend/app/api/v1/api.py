from fastapi import APIRouter
from app.api.v1.endpoints import auth, documents, analysis, career_paths, users, test

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(career_paths.router, prefix="/career-paths", tags=["career-paths"])
api_router.include_router(test.router, prefix="/test", tags=["test"])