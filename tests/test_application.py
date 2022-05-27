from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from pydantic import AnyHttpUrl

from fastapi_asyncapi import get_asyncapi, get_asyncapi_html

app = FastAPI(title="MyAPI", version="1.0.0", docs_url=None)


@app.get("/asyncapi.json", include_in_schema=False)
async def asyncapi_json():
    return JSONResponse(
        get_asyncapi(title=app.title, version=app.version, routes=app.routes),
        media_type="application/vnd.aai.asyncapi+json;version=2.4.0",
    )


@app.get("/docs", tags=["Docs"])
async def asyncapi_docs():
    asyncapi_url = AnyHttpUrl("asyncapi.json", scheme="http")
    return get_asyncapi_html(asyncapi_url=asyncapi_url, title=app.title)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


def test_application():
    schema = get_asyncapi(title=app.title, version=app.version, routes=app.routes)
    # import json

    # print(json.dumps(schema, indent=4, sort_keys=True))
    assert schema == {
        "asyncapi": "2.2.0",
        "channels": {
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
                    "operationId": "asyncapi_docs_docs_get",
                    "tags": [{"name": "Docs"}],
                },
            },
            "/ws": {
                "subscribe": {
                    "bindings": {"ws": {"bindingVersion": "latest", "method": "GET"}},
                    "operationId": "websocket_endpoint",
                }
            },
        },
        "defaultContentType": "application/json",
        "info": {"title": "MyAPI", "version": "1.0.0"},
    }
