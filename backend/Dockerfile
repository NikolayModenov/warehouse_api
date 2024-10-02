FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir --upgrade
COPY . .
CMD ["uvicorn", "main:APP", "--host", "0.0.0.0", "--port", "80"]