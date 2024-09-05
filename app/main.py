# 라우터를 포함하고 서버를 실행 시킨다
import uvicorn
from fastapi import FastAPI

import app.router.analysis_router as analysis_router

# FastAPI 애플리케이션(app) 초기화
app = FastAPI()

# FastAPI 의 router를 등록
app.include_router(analysis_router.router)
# 실행
if __name__ == "__main__":
    uvicorn.run(app, port=8000)