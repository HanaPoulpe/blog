FROM python:3.13-bookworm AS base

# Install system deps
ARG debug=0
ENV DEBUG=${debug}
RUN echo "Debug mode: $DEBUG"
RUN apt update && apt upgrade -y --no-install-recommends
RUN test "$DEBUG" -eq 1 && \
    apt install -y shellcheck --no-install-recommends;
# Cleanup apt cache
RUN rm -rf /var/lib/apt/lists/*
# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

FROM base AS build
WORKDIR /src
COPY uv.lock pyproject.toml README.md ./
COPY src ./src/
COPY requirements ./requirements

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

# Build
RUN uv build -o ./build

# Finalize
FROM base AS release
WORKDIR /app

COPY --from=build /src/build /app/build
RUN pip install ./build/*.whl
RUN rm -rf /app/build

RUN useradd -ms /bin/bash blog
USER blog

COPY deployment/entrypoint.sh deployment/tests.sh /app/

WORKDIR /app/blog
COPY src/manage.py .

ENV PYTHONPATH=/app/blog
ENV ENTRYPOINT=/app/entrypoint.sh
ENV DJANGO_SETTINGS_MODULE=blog.settings

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
