FROM python:3.12-alpine
ARG FLASK_PORT=5100
ARG REDIS_HOST=localhost
ARG REDIS_PORT=30079
ENV FLASK_PORT=$FLASK_PORT
ENV REDIS_HOST=$REDIS_HOST
ENV REDIS_PORT=$REDIS_PORT
RUN apk update
RUN adduser -D mgbackcountry
USER mgbackcountry
ENV PATH=/home/mgbackcountry/.local/bin:$PATH
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD flask --app app run --debug --host 0.0.0.0 --port ${FLASK_PORT}
