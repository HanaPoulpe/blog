# Hana's wagtail blog

![python](https://img.shields.io/static/v1?label=Python&message=3.12&logo=Python&color=3776AB)
[![python-tests](https://github.com/HanaPoulpe/blog/actions/workflows/python-test.yml/badge.svg)](https://github.com/HanaPoulpe/blog/actions/workflows/python-test.yml)
[![CodeQL](https://github.com/HanaPoulpe/blog/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/HanaPoulpe/blog/actions/workflows/github-code-scanning/codeql)
[![codecov](https://codecov.io/github/HanaPoulpe/blog/graph/badge.svg?token=D5J8G4P5RC)](https://codecov.io/github/HanaPoulpe/blog)

# How to setup
## Install dependencies:

```shell
pip install -r requirements.txt
poetry install --with dev
```

## Setup pre-commit

```shell
pre-commit install
cp .pre-commit-config.yaml.example .pre-commit-config.yaml
```

Select your precommit hooks.

## Setup commit-linter

```shell
pre-commit install --hook-type commit-msg
```

Then enable the `Commit lint` section from your `.pre-commit-config.yaml`.

## Run tests:

```shell
poetry run python-all-tests
```

# Django:

## Migrations

Create migration files with

```shell
poetry run django-makemigrations
```

Apply migrations:
```shell
poetry run django-migrate --configuration=BlogSite
```

## Run server

```shell
poetry run django-start --host=0.0.0.0 --port=8000
```

## `manage.py`

```shell
poetry run django-manage --configuration=BlogSite
```
