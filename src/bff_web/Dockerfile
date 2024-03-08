FROM python:3.10

EXPOSE 8000/tcp

COPY bff-requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip pip install -r bff-requirements.txt

COPY ./src /src

WORKDIR "/src"

CMD [ "uvicorn", "bff_web.main:app", "--host=0.0.0.0"]