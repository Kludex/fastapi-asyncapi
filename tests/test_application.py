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


def test_application():
    schema = get_asyncapi(title=app.title, version=app.version, routes=app.routes)
    # print(json.dumps(schema, indent=4, sort_keys=True))
    assert schema == {
        "asyncapi": "2.4.0",
        "channels": {
            "/asyncapi.json": {
                "description": "",
                "subscribe": {
                    "bindings": {
                        "http": {
                            "bindingVersion": "latest",
                            "method": "GET",
                            "type": "request",
                        }
                    },
                    "operationId": "asyncapi_json",
                },
            },
            "/docs": {
                "description": "",
                "subscribe": {
                    "bindings": {
                        "http": {
                            "bindingVersion": "latest",
                            "method": "GET",
                            "type": "request",
                        }
                    },
                    "operationId": "asyncapi_docs",
                },
            },
        },
        "info": {"title": "MyAPI", "version": "1.0.0"},
    }
