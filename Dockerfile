FROM python:3.13.3-slim-bookworm

WORKDIR /app
COPY . /app

COPY requirements.txt ./
COPY chainlit.md ./
COPY main.py ./

RUN pip install --upgrade pip && pip install chainlit pydantic_ai httpx python-dotenv

EXPOSE 8080

ENTRYPOINT ["chainlit", "run", "--host","main.py", "0.0.0.0", "--port", "8080"]
