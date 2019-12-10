FROM python:3

WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y sqlite
COPY ./ ./

EXPOSE 31337:31337
CMD ["python", "./main.py"]
