FROM python:3.12-alpine
RUN apk update
RUN adduser -D mgbackcountry
USER mgbackcountry
ENV PATH /home/mgbackcountry/.local/bin:$PATH
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["flask", "--app", "app", "run", "--debug", "--host", "0.0.0.0"]
#ENTRYPOINT ["top", "-b"]
