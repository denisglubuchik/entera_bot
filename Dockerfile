FROM python:latest
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "/app/bot.py"]