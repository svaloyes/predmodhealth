FROM python:3.8.13 as base

ENV PYTHONPATH=$PYTHONPATH:/src/api
ENV PATH=$PATH:/home/app/.local/bin/

COPY ./ /src

WORKDIR /src

RUN pip install --upgrade pip && pip install -r requirements.txt

FROM base as build
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
