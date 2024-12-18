FROM python:3.12.3
RUN apt-get update && apt-get install -y curl && apt-get install -y iputils-ping
WORKDIR /app/ 
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY .env /app/.env
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]