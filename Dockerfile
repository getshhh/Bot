FROM python:3.8
WORKDIR /app/code
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
COPY ./app /app/code
CMD ["python", "-u", "/app/code/bot.py"]
