# FastAPI-AsyncAPI

FastAPI-AsyncAPI is a utility tool to write documentation for your [FastAPI](https://fastapi.tiangolo.com/) endpoints using [AsyncAPI](https://github.com/asyncapi/spec).

It provides support for WebSockets, which is currently missing in OpenAPI.

## Usage

```python
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
