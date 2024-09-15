FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev
COPY . .
EXPOSE 5000
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
