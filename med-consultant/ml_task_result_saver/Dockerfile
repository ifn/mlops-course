FROM python:3.10-slim

WORKDIR /ml_task_result_saver

COPY requirements.txt /ml_task_result_saver/

RUN pip install --upgrade pip && pip install -r /ml_task_result_saver/requirements.txt

CMD ["python", "-u", "main.py"]
