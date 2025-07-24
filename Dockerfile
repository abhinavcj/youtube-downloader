FROM python:3.13-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]
