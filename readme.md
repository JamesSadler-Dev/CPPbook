<h1>CPPbook- learnCPP converter</h1>

[![Build and Test](https://github.com/JamesSadler-Dev/CPPbook/actions/workflows/build-test.yml/badge.svg)](https://github.com/JamesSadler-Dev/CPPbook/actions/workflows/build-test.yml)

<h3>Usage:</h3>

<li>Install dependencies with poetry:</li>

```bash
poetry install
```

<li>Run program to generate all require files:</ii><br>

```bash
poetry run python ./learncppbook/getCPPbook.py
```

<li>Run flask backend server:</li>

```bash
poetry run python -m flask run
```

Note: use a production ASGI server for any professional use.