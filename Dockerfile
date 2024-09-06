# 베이스 이미지로 Python 3.9 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt /app/

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 애플리케이션 파일을 복사
COPY ./app /app

# 외부 접근을 위한 포트 8000 열기
EXPOSE 8000

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
