FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY chat/ ./chat/
COPY src/ ./src/
COPY LLM_Connection.py .
COPY datos.sqlite .

EXPOSE 8000

CMD ["uvicorn", "chat.main:app", "--host", "0.0.0.0", "--port", "8000"]
