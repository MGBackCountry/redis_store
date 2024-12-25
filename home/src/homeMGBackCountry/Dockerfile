FROM python:3.12-alpine

ARG FLASK_RUN_PORT=5100
ARG REDIS_HOST=redis-service
ARG REDIS_PORT=6379

ENV FLASK_RUN_PORT=$FLASK_RUN_PORT
ENV REDIS_HOST=$REDIS_HOST
ENV REDIS_PORT=$REDIS_PORT
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST="0.0.0.0"

RUN apk update
RUN adduser -D mgbackcountry
USER mgbackcountry
EXPOSE ${FLASK_PORT}
ENV PATH=/home/mgbackcountry/.local/bin:$PATH
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["flask", "run", "--debug"]

