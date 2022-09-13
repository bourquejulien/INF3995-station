FROM python:3.10-slim as build
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc git

WORKDIR /usr/app
RUN python -m venv /usr/src/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.10-slim as final
EXPOSE 5000/tcp

WORKDIR /usr/app
COPY --from=build /usr/app/venv ./venv
COPY . .

ENV PATH="/usr/app/venv/bin:$PATH"
ENTRYPOINT ["python"]
CMD ["app.py"]
