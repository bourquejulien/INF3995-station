FROM python:3.10-slim AS base

RUN apt update && apt install -y --no-install-recommends curl

HEALTHCHECK --interval=1m --timeout=3s \
  CMD curl -f "http://localhost:5000/health" || exit 1

FROM python:3.10-slim AS build

RUN apt update && apt install -y --no-install-recommends build-essential gcc git

WORKDIR /usr/app
RUN python -m venv ./venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY protos/simulation.proto protos/simulation.proto
COPY ./requirements.* ./
RUN python3 requirements.py

COPY . .

FROM base AS final
EXPOSE 5000/tcp

WORKDIR /usr/app
COPY --from=build /usr/app/ .

ENV PATH="/usr/app/venv/bin:$PATH"
ENTRYPOINT ["python"]
CMD ["app.py"]

FROM build AS test

ENV IS_SIMULATION=False

ENTRYPOINT ["pytest", "tests"]

