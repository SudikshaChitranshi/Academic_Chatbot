from fastapi import APIRouter, Request
from app.services.jsjiit_client import get_cgpa_sgpa

router = APIRouter()

@router.post("/get-cgpa")
async def get_cgpa_route(request: Request):
    body = await request.json()
    enrollment = body.get("enrollment")
    password = body.get("password")
    
    result = await get_cgpa_sgpa(enrollment, password)
    return result
