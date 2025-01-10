FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update 
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
