FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY your_script.py .

CMD ["python", "your_script.py", "--data-dir", "/app/data", "--out-dir", "/app/out"]
