from typing import Any, Dict, List, Literal, Optional, Sequence

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute, APIWebSocketRoute
from pydantic import AnyHttpUrl
from starlette.routing import BaseRoute

from fastapi_asyncapi.schema import (
    AsyncAPI,
    Bindings,
    ChannelItem,
    Channels,
    Contact,
    HTTPOperationBinding,
    Info,
    License,
    Server,
    Subscribe,
    Tag,
    WSOperationBinding,
)


def get_asyncapi(
    *,
    title: str,
    version: str,
    routes: Sequence[BaseRoute],
    asyncapi_version: Literal["2.4.0"] = "2.4.0",
    id: Optional[str] = None,
    description: Optional[str] = None,
    terms_of_service: Optional[AnyHttpUrl] = None,
    contact: Optional[Contact] = None,
    license: Optional[License] = None,
    tags: Optional[List[Tag]] = None,
    servers: Optional[List[Server]] = None,
) -> Dict[str, Any]:
    info = Info(
        title=title,
        version=version,
        description=description,
        termsOfService=terms_of_service,
        contact=contact,
        license=license,
    )
    channels: Channels = {}
    for route in routes:
        if isinstance(route, APIRoute):
            channel = ChannelItem(
                ref=route.path,
                description=route.description,
                subscribe=Subscribe(
                    operationId=route.endpoint.__name__,  # TODO: Copy FastAPI here.
                    bindings=Bindings(
                        http=HTTPOperationBinding(
                            type="request", method=next(iter(route.methods))
                        )
                    ),
                ),
            )
            channels[route.path] = channel
        elif isinstance(route, APIWebSocketRoute):
            channel = ChannelItem(
                ref=route.path,
                subscribe=Subscribe(
                    operationId=route.endpoint.__name__,  # TODO: Copy FastAPI here.
                    bindings=Bindings(ws=WSOperationBinding()),
                ),
            )
            channels[route.path] = channel

    return jsonable_encoder(
        AsyncAPI(
            asyncapi=asyncapi_version,
            id=id,
            info=info,
            tags=tags,
            servers=servers,
            channels=channels,
        ),
        by_alias=True,
        exclude_none=True,
    )


def get_asyncapi_html(
    *,
    asyncapi_url: AnyHttpUrl,
    title: str,
    asyncapi_js_url: str = "https://unpkg.com/@asyncapi/web-component@0.24/lib/asyncapi-web-component.js",  # noqa: E501
    asyncapi_css_url: str = "https://unpkg.com/@asyncapi/react-component@0.24/lib/styles/fiori.css",  # noqa: E501
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
