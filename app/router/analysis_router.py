from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse
# from app.model.analysis_model import analysis_model

router = APIRouter()


class Diary(BaseModel):
    content: str


@router.post("/analysis")
async def analysis_router(diary: Diary):
    content = diary.content
    if content is None:
        return JSONResponse({"error": "본문이 제공되지 않습니다.", "content": content}, status_code=400)
    # 일기 내용을 받아서 사용

    # response = analysis_model() 분석 함수
    return JSONResponse(content=content)
