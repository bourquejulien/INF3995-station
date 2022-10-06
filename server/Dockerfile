FROM python:3.10-slim AS build
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc git

WORKDIR /usr/app
RUN python -m venv ./venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY . .
COPY ./requirements.py .
COPY ./requirements.txt .
RUN python3 requirements.py

COPY . .

FROM python:3.10-slim AS final
EXPOSE 5000/tcp

WORKDIR /usr/app
COPY --from=build /usr/app/ .

ENV PATH="/usr/app/venv/bin:$PATH"
ENTRYPOINT ["python"]
CMD ["app.py"]

FROM build AS test

ENV IS_SIMULATION=False

ENTRYPOINT ["pytest", "tests"]
