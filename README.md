<h1 align="center">
    <strong>FastAPI-AsyncAPI</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/fastapi-asyncapi" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/fastapi-asyncapi" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/Kludex/fastapi-asyncapi/Test">
        <img src="https://img.shields.io/codecov/c/github/Kludex/fastapi-asyncapi">
    <br />
    <a href="https://pypi.org/project/fastapi-asyncapi" target="_blank">
        <img src="https://img.shields.io/pypi/v/fastapi-asyncapi" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/fastapi-asyncapi">
    <img src="https://img.shields.io/github/license/Kludex/fastapi-asyncapi">
</p>

FastAPI-AsyncAPI is a utility tool to write documentation for your [FastAPI](https://github.com/tiangolo/fastapi) endpoints using [AsyncAPI](https://github.com/asyncapi).

It provides support for WebSockets, which is currently missing in OpenAPI.


> This package is not completed. Help is wanted.

## Installation

``` bash
pip install fastapi-asyncapi
```

## Usage

``` python
from fastapi import FastAPI
from pydantic import AnyHttpUrl

from fastapi_asyncapi import get_asyncapi, get_asyncapi_html

app = FastAPI(title="MyAPI", version="1.0.0", docs_url=None)


@app.get("/asyncapi.json")
async def asyncapi_json():
    return get_asyncapi(title=app.title, version=app.version, routes=app.routes)


@app.get("/docs")
async def asyncapi_docs():
    asyncapi_url = AnyHttpUrl("asyncapi.json", scheme="http")
    return get_asyncapi_html(asyncapi_url=asyncapi_url, title=app.title)
```


## License

This project is licensed under the terms of the MIT license.
