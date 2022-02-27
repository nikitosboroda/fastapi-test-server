FROM python:3.8-slim

WORKDIR /calc

COPY ./src /calc/src
COPY requirements.txt /tmp

#RUN python -m pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

CMD ["uvicorn", "src.api.server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]