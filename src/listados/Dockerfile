FROM python:3.10
ENV LC_ALL en_US.UTF-8

EXPOSE 5000/tcp

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY ./src /src
WORKDIR /

CMD [ "flask", "--app", "/src/listados/api", "run", "--host=0.0.0.0"]
