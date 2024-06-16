# Hana's wagtail blog

![python](https://img.shields.io/static/v1?label=Python&message=3.12&logo=Python&color=3776AB)
[![python-tests](https://github.com/HanaPoulpe/blog/actions/workflows/run-python-tests.yml/badge.svg)](https://github.com/HanaPoulpe/blog/actions/workflows/run-python-tests.yml)
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
