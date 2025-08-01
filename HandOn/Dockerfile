# syntax=docker/dockerfile:1.4
FROM python:3.12-slim

ARG APP_PORT=5000
ARG APP_VERSION=1.0.0

LABEL maintainer="Yash Bansal <yash@example.com>" \
      app.version=$APP_VERSION

ENV APP_PORT=$APP_PORT \
    CONFIG_PATH=/app/app/config.json

WORKDIR /app

COPY app/ ./app/
COPY requirements.txt ./

ADD assets/banner.png /app/public/banner.png

VOLUME /app/data

EXPOSE $APP_PORT

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:$APP_PORT/health || exit 1

RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y curl

USER root

ONBUILD COPY . /src

ENTRYPOINT ["python"]
CMD ["app/server.py"]






