from typing import Dict, List, Literal, Optional, TypedDict, Union

from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from pydantic.networks import AnyHttpUrl, EmailStr

get_openapi()


class Contact(TypedDict):
    name: Optional[str]
    url: Optional[AnyHttpUrl]
    email: Optional[EmailStr]


class ExternalDocumentation(TypedDict):
    description: Optional[str]
    url: AnyHttpUrl


class Tag(TypedDict):
    name: str
    description: Optional[str]
    externalDocs: Optional[ExternalDocumentation]


class License(TypedDict):
    name: str
    url: Optional[str]


class Info(TypedDict):
    title: str
    version: str
    description: Optional[str]
    termsOfService: Optional[AnyHttpUrl]
    contact: Optional[Contact]
    license: Optional[License]


Protocol = Literal[
    "amqp",
    "amqps",
    "http",
    "https",
    "jms",
    "kafka",
    "kafka-secure",
    "mqtt",
    "secure-mqtt",
    "stomp",
    "stomps",
    "ws",
    "wss",
]


class ServerVariable(TypedDict):
    enum: Optional[List[str]]
    default: str
    description: Optional[str]
    examples: Optional[List[str]]


HTTPMethod = Literal[
    "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "CONNECT", "TRACE"
]


class HTTPOperationBinding(TypedDict):
    type: Literal["request", "response"]
    method: HTTPMethod
    # query: # Missing this
    bindingVersion: Union[Literal["latest"], str]


class OperationBinding(TypedDict):
    http: Optional[HTTPOperationBinding]
    # Missing remaining


Bindings = Dict[str, OperationBinding]


class Operation(TypedDict):
    operationId: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    tags: List[Tag]
    externalDocs: Optional[ExternalDocumentation]
    bindings: Optional[Bindings]


Subscribe = Operation
Publish = Operation


class Channel(TypedDict):
    ref: Optional[str]  # alias="$ref"
    description: Optional[str]
    subscribe: Optional[Subscribe]
    publish: Optional[Publish]


Security = Dict[str, List[str]]
Channels = List[Dict[str, Channel]]


class Server(TypedDict):
    url: str
    protocol: Protocol
    protocolVersion: Optional[str]
    description: Optional[str]
    variables: Optional[List[Dict[str, ServerVariable]]]
    security: Optional[List[Security]]
    channels: Channels


class AsyncAPI(TypedDict):
    asyncapi: str
    id: str
    info: Info
    servers: Optional[List[Dict[str, Server]]]  # Validate str on Dict[str, ...]


def get_asyncapi(
    *,
    title: str,
    version: str,
    description: Optional[str] = None,
    termsOfService: Optional[AnyHttpUrl] = None,
    contact: Optional[Contact] = None,
    tags: Optional[List[Tag]] = None,
    # server: Optional[List[Server]] = None,
):
    ...


def get_asyncapi_html(
    *,
    asyncapi_url: AnyHttpUrl,
    title: str,
    asyncapi_js_url: AnyHttpUrl = "https://unpkg.com/@asyncapi/web-component@0.19.0/lib/asyncapi-web-component.js",
    asyncapi_css_url: AnyHttpUrl = "https://unpkg.com/@asyncapi/react-component@0.19.0/lib/styles/fiori.css",
):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <script src="{asyncapi_js_url}" defer></script>

        <asyncapi-component
            schemaUrl="{asyncapi_url}"
            cssImportPath="{asyncapi_css_url}">
        </asyncapi-component>
    </body>
    </html>
    """
    return HTMLResponse(html)
