import json
import os
from fastapi import HTTPException
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse
from app.model.analysis_model import analysis

router = APIRouter()


class Diary(BaseModel):
    content: str


# 현재 스크립트의 디렉토리를 기준으로 상대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'data')

# JSON 데이터 로드
try:
    with open(os.path.join(data_dir, "emotionTypeDescriptions.json"), "r", encoding="utf-8") as f:
        emotionTypeDescriptions = json.load(f)
except FileNotFoundError:
    emotionTypeDescriptions = {}
    print("Error : emotionTypeDescriptions.json 파일을 찾을 수 없습니다.")
    raise HTTPException(status_code=400, detail="emotionTypeDescriptions.json 파일을 찾을 수 없습니다.")

try:
    with open(os.path.join(data_dir, "typeDescription.json"), "r", encoding="utf-8") as f:
        typeDescriptions = json.load(f)
except FileNotFoundError:
    print("Error : typeDescription.json 파일을 찾을 수 없습니다.")
    raise HTTPException(status_code=400, detail="typeDescription.json 파일을 찾을 수 없습니다.")


def get_default_response():
    return {
        "rjmd": {
            "R": get_default_type_data(),
            "J": get_default_type_data(),
            "M": get_default_type_data(),
            "D": get_default_type_data()
        },
        "emotions": [
            {
                "name": "없음",
                "per": 100,
                "desc": ["감정을 분석할 수 없습니다."],
                "color": "#808080"
            }
        ],
        "happy": {"per": 0}
    }


def get_default_type_data():
    return {
        "type": "N",  # Neutral
        "per": 100,
        "desc": "분석할 수 없습니다."
    }


@router.post("/analysis")
async def analysis_router(diary: Diary) -> JSONResponse:
    content = diary.content
    if content is None:
        return JSONResponse({"error": "본문이 비어있습니다.", "content": content}, status_code=400)
    try:
        response = json.loads(analysis(content))

        if not response or "rjmd" not in response:
            # 기본값 설정
            response = get_default_response()

        rjmd = response["rjmd"]

        for key in ["R", "J", "M", "D"]:
            if key not in rjmd or "type" not in rjmd[key]:
                rjmd[key] = get_default_type_data()

            type_value = rjmd[key]["type"]
            rjmd[key]["title"] = typeDescriptions[key][type_value]["title"]
            rjmd[key]["desc"] = typeDescriptions[key][type_value]["description"]

        type_combination = f"{rjmd['R']['type']}{rjmd['J']['type']}{rjmd['M']['type']}{rjmd['D']['type']}"
        rjmd["title"] = emotionTypeDescriptions[type_combination]["title"]
        rjmd["desc"] = emotionTypeDescriptions[type_combination]["description"]
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="분석 결과를 JSON으로 파싱하는데 실패했습니다.")
    except Exception as e:
        error_message = str(e)
        if "Message content must be non-empty" in error_message:
            raise HTTPException(status_code=400, detail="분석할 내용이 비어 있습니다. 유효한 텍스트를 입력해 주세요.")
        elif "invalid_request_error" in error_message:
            raise HTTPException(status_code=400, detail="잘못된 요청입니다. 입력 내용을 확인해 주세요.")
        else:
            raise HTTPException(status_code=500, detail=f"일기 분석 중 오류가 발생했습니다: {error_message}")

    return JSONResponse(
        content=response,
        media_type="application/json",
        headers={"Content-Type": "application/json; charset=utf-8"}, status_code=200
    )
