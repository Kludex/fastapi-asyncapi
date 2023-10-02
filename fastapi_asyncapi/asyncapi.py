from inspect import cleandoc
from typing import Any, Dict, List, Literal, Optional, Sequence, cast

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
    HTTPMethod,
    HTTPOperationBinding,
    Info,
    License,
    Operation,
    Server,
    Tag,
    WSOperationBinding, Reference, Components, Message, OneOf,
)


class SubscribeMessage:
    pass


class PublishMessage:
    pass


def get_asyncapi(
        *,
        title: str,
        version: str,
        routes: Sequence[BaseRoute],
        asyncapi_version: Literal["2.2.0"] = "2.2.0",
        id: Optional[str] = None,
        description: Optional[str] = None,
        terms_of_service: Optional[AnyHttpUrl] = None,
        contact: Optional[Contact] = None,
        license: Optional[License] = None,
        tags: Optional[List[Tag]] = None,
        servers: Optional[Dict[str, Server]] = None,
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
    messages: dict[str, Message] = {}

    for route in routes:
        if isinstance(route, APIRoute) and route.include_in_schema:
            channel = ChannelItem(
                ref=route.path,
                description=route.description,
                subscribe=Operation(
                    tags=[Tag(name=str(tag)) for tag in route.tags],
                    operationId=route.unique_id,
                    bindings=Bindings(
                        http=HTTPOperationBinding(
                            type="request", method=cast(HTTPMethod, min(route.methods))
                        )
                    ),
                ),
            )
            channels[route.path] = channel
        elif isinstance(route, APIWebSocketRoute):
            msgs = {'subscribe': [], 'publish': []}
            for dep in route.dependant.body_params:
                kind = None
                if isinstance(dep.default, SubscribeMessage):
                    kind = 'subscribe'
                elif isinstance(dep.default, PublishMessage):
                    kind = 'publish'
                else:
                    continue

                msg = dep.field_info.annotation
                if msg is None:
                    continue
                msgs[kind].append(Reference(**{'$ref': f"#/components/messages/{msg.__name__}"}))
                messages[msg.__name__] = Message(
                    description=msg.__doc__,
                    payload=msg.model_json_schema(),
                )

            doc = None
            if callable(route.dependant.cache_key[0]):
                doc = cleandoc(route.dependant.cache_key[0].__doc__)
            channel = ChannelItem(
                ref=route.path,
                description=doc,
                subscribe=Operation(
                    operationId=f"{route.name}_subscribe",
                    bindings=Bindings(ws=WSOperationBinding()),
                ),
            )
            if len(msgs['subscribe']) > 0:
                subs = msgs['subscribe']
                subs = subs[0] if len(subs) == 1 else OneOf(oneOf=subs)
                channel.subscribe.message = subs
            if len(msgs['publish']) > 0:
                pubs = msgs['publish']
                pubs = pubs[0] if len(pubs) == 1 else OneOf(oneOf=pubs)
                channel.publish = Operation(
                    operationId=f"{route.name}_publish",
                    bindings=Bindings(ws=WSOperationBinding()),
                    message=pubs,
                )
            channels[route.path] = channel

    components = None
    if len(messages) > 0:
        components = Components(
            messages=messages,
        )

    return jsonable_encoder(
        AsyncAPI(
            asyncapi=asyncapi_version,
            id=id,
            info=info,
            tags=tags,
            servers=servers,
            channels=channels,
            components=components,
        ),
        by_alias=True,
        exclude_none=True,
    )


def get_asyncapi_html(
        *,
        asyncapi_url: AnyHttpUrl,
        title: str,
        asyncapi_js_url: str = "https://unpkg.com/@asyncapi/react-component@latest/browser/standalone/index.js",
        # noqa: E501
        asyncapi_css_url: str = "https://unpkg.com/@asyncapi/react-component@latest/styles/default.min.css",
        # noqa: E501
):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="{asyncapi_css_url}">
    </head>
    <body>
    
        <div id="asyncapi"></div>

        <script src="{asyncapi_js_url}"></script>
        <script>
          AsyncApiStandalone.render({{
            schema: {{
              url: '{asyncapi_url}',
              options: {{ method: "GET", mode: "cors" }},
            }},
            config: {{
              show: {{
                sidebar: true,
              }}
            }},
          }}, document.getElementById('asyncapi'));
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)
