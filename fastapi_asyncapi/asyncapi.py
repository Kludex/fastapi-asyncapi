from typing import Any, Dict, List, Optional, Sequence

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from pydantic import AnyHttpUrl
from starlette.routing import BaseRoute

from fastapi_asyncapi.schema import (
    AsyncAPI,
    Channels,
    Contact,
    Info,
    License,
    Server,
    Tag,
)


def get_asyncapi(
    *,
    title: str,
    version: str,
    routes: Sequence[BaseRoute],
    asyncapi_version: str = "2.0.0",
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
            print(route.endpoint)

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


app = FastAPI(title="MyAPI", version="1.0.0", docs_url=None)


@app.get("/asyncapi.json")
async def asyncapi_json():
    return get_asyncapi(title=app.title, version=app.version, routes=app.routes)


@app.get("/docs")
async def asyncapi_docs():
    asyncapi_url = AnyHttpUrl("http://localhost:8000/asyncapi.json", scheme="http")
    return get_asyncapi_html(asyncapi_url=asyncapi_url, title=app.title)
