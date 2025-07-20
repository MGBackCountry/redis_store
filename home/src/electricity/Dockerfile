FROM python:alpine3.22

WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ARG FLASK_RUN_PORT=5100
ARG REDIS_HOST=redis-service
ARG REDIS_PORT=6379

ENV FLASK_RUN_PORT=$FLASK_RUN_PORT
ENV REDIS_HOST=$REDIS_HOST
ENV REDIS_PORT=$REDIS_PORT
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST="0.0.0.0"
ENV PATH=/home/mgbackcountry/.local/bin:$PATH

RUN apk update && adduser -D mgbackcountry
USER mgbackcountry

EXPOSE ${FLASK_RUN_PORT}
CMD ["flask", "run", "--debug"]

