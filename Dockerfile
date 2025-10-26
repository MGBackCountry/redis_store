FROM python:3.14.0-alpine3.22

WORKDIR /app/electricity
COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev && \
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY electricity/ .

ARG FLASK_RUN_PORT
ARG REDIS_HOST
ARG REDIS_PORT

ENV FLASK_RUN_PORT=${FLASK_RUN_PORT:-5100}
ENV REDIS_HOST=${REDIS_HOST:-redis}
ENV REDIS_PORT=${REDIS_PORT:-6379}
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PATH=/home/mgbackcountry/.local/bin:$PATH

RUN apk update && adduser -D mgbackcountry
USER mgbackcountry

EXPOSE ${FLASK_RUN_PORT}
ENTRYPOINT ["flask", "run", "--debug"]

