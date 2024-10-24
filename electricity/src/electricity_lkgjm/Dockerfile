FROM python:3.12-alpine
EXPOSE 5000
RUN apk update
RUN adduser -D lkgjm
USER lkgjm
ENV PATH /home/lkgjm/.local/bin:$PATH
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["flask", "--app", "app", "run", "--debug", "--host", "0.0.0.0"]
#ENTRYPOINT ["top", "-b"]
