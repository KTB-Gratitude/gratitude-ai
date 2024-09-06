import json
import os
from fastapi import HTTPException
from fastapi import APIRouter
from openai import InternalServerError
from pydantic import BaseModel
from starlette.responses import JSONResponse
from app.model.analysis_model import analysis
import openai

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
            "R": get_default_type_data("R"),
            "J": get_default_type_data("J"),
            "M": get_default_type_data("M"),
            "D": get_default_type_data("D")
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


def get_default_type_data(key):
    target_key, _ = typeDescriptions[key].keys()
    return {
        "type": target_key,  # Neutral
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
        print(response)
        rjmd = response["rjmd"]

        for key in ["R", "J", "M", "D"]:
            if key not in rjmd or "type" not in rjmd[key]:
                rjmd[key] = get_default_type_data(key)

            type_value = rjmd[key]["type"]
            rjmd[key]["title"] = typeDescriptions[key][type_value]["title"]
            rjmd[key]["desc"] = typeDescriptions[key][type_value]["description"]

        type_combination = f"{rjmd['R']['type']}{rjmd['J']['type']}{rjmd['M']['type']}{rjmd['D']['type']}"
        rjmd["title"] = emotionTypeDescriptions[type_combination]["title"]
        rjmd["desc"] = emotionTypeDescriptions[type_combination]["description"]
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"분석 결과를 JSON으로 파싱하는데 실패했습니다. - {str(e)}")
    except openai.BadRequestError as e:
        raise HTTPException(status_code=400, detail=f"잘못된 요청입니다. 입력 내용을 확인해 주세요. - {str(e)}")
    except openai.APITimeoutError as e:
        raise HTTPException(status_code=400, detail=f"OpenAI API 시간 초과 - {str(e)}")
    except openai.AuthenticationError as e:
        raise HTTPException(status_code=400, detail=f"OpenAI API 인증 실패 - {str(e)}")
    except openai.InternalServerError as e:
        raise HTTPException(status_code=400, detail=f"내부 서버 오류 - {str(e)} ")
    except openai.APIConnectionError as e:
        raise HTTPException(status_code=400, detail=f"OpenAI API 연결 실패 - {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

    return JSONResponse(
        content=response,
        media_type="application/json",
        headers={"Content-Type": "application/json; charset=utf-8"}, status_code=200
    )
