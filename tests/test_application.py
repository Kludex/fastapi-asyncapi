from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from fastapi_asyncapi import get_asyncapi, get_asyncapi_html, SubscribeMessage, PublishMessage

app = FastAPI(title="MyAPI", version="1.0.0", docs_url=None)


@app.get("/asyncapi.json", include_in_schema=False)
async def asyncapi_json():
    return JSONResponse(
        get_asyncapi(title=app.title, version=app.version, routes=app.routes),
        media_type="application/vnd.aai.asyncapi+json;version=2.4.0",
    )


@app.get("/docs", tags=["Docs"])
async def asyncapi_docs():
    return get_asyncapi_html(asyncapi_url="asyncapi.json", title=app.title)


class MyMessage(BaseModel):
    kind: str


class MyMessage2(BaseModel):
    text: str


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, msg: MyMessage = SubscribeMessage(),
                             m2: MyMessage = PublishMessage(), m3: MyMessage2 = PublishMessage()):
    """
    This endpoint creates a websocket connection to the service.
    """
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
                "description": "This endpoint creates a websocket connection to the service.",
                "subscribe": {
                    "bindings": {"ws": {"bindingVersion": "latest", "method": "GET"}},
                    "operationId": "websocket_endpoint_subscribe",
                    "message": {"$ref": "#/components/messages/MyMessage"},
                },
                "publish": {
                    "operationId": "websocket_endpoint_publish",
                    "bindings": {"ws": {"method": "GET", "bindingVersion": "latest"}},
                    "message": {
                        "oneOf": [
                            {"$ref": "#/components/messages/MyMessage"},
                            {"$ref": "#/components/messages/MyMessage2"}
                        ]
                    }
                }
            },
        },
        "defaultContentType": "application/json",
        "info": {"title": "MyAPI", "version": "1.0.0"},
        "components": {
            "messages": {
                "MyMessage": {
                    "payload": {
                        "properties": {"kind": {"title": "Kind", "type": "string"}},
                        "required": ["kind"],
                        "title": "MyMessage",
                        "type": "object"
                    }
                },
                "MyMessage2": {
                    "payload": {
                        "properties": {"text": {"title": "Text", "type": "string"}},
                        "required": ["text"],
                        "title": "MyMessage2",
                        "type": "object"
                    }
                }
            }
        }
    }
