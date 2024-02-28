FROM python:3.10

EXPOSE 5000/tcp

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src /src
WORKDIR /

CMD [ "flask", "--app", "/src/listados/api", "run", "--host=0.0.0.0"]
