FROM python:3.12-bookworm AS base

# Install system deps
ARG debug
ENV DEBUG=${debug}
RUN echo "Debug mode: $DEBUG"
RUN apt update && apt upgrade -y --no-install-recommends
RUN test $DEBUG -eq 1 && \
    apt install -y shellcheck --no-install-recommends;
# Cleanup apt cache
RUN rm -rf /var/lib/apt/lists/*

FROM base AS build
WORKDIR /src
COPY poetry.lock pyproject.toml README.md ./
COPY src ./src/
COPY requirements ./requirements

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

# Install python build
RUN pip install -r ./requirements/common.txt

RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main --no-root && \
    poetry build

# Finalize
FROM base AS release
WORKDIR /app

COPY --from=build /src/.venv /app/venv
COPY --from=build /src/dist /app/dist
RUN pip install ./dist/*.whl
RUN rm -rf /app/venv /app/dist

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
