FROM python:3.10-slim

WORKDIR /api

COPY requirements.txt /api/

RUN pip install --upgrade pip && pip install -r /api/requirements.txt

EXPOSE 8080

CMD ["python", "-u", "api.py"]
