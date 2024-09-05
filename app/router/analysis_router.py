import openai
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/analysis")
async def analysis(request: Request):
    # 일기 내용을 받아서 사용
    pass