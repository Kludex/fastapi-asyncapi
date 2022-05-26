import json

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
def home():
    html_page = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <!-- Remove 'webcomponentsjs' if no support for older browsers is required -->
        <script src="https://unpkg.com/@asyncapi/web-component@0.19.0/lib/asyncapi-web-component.js" defer></script>  # noqa: E501

        <asyncapi-component
            schemaUrl="http://localhost:8000/asyncapi.json"
            cssImportPath="https://unpkg.com/@asyncapi/react-component@0.19.0/lib/styles/fiori.css">
        </asyncapi-component>
    </body>
    </html>
    """
    return HTMLResponse(html_page)


@app.get("/asyncapi.json")
def asyncapi_json():
    asyncapi = {
        "asyncapi": "2.0.0",
        "info": {
            "title": "Example",
            "version": "0.1.0",
            "contact": {
                "name": "API Support",
                "url": "http://www.example.com/support",
                "email": "support@example.com",
            },
        },
        "channels": {
            "user/signedup": {
                "subscribe": {
                    "message": {
                        "description": "An event describing.",
                        "payload": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "fullName": {"type": "string"},
                                "email": {"type": "string", "format": "email"},
                                "age": {"type": "integer", "minimum": 18},
                            },
                        },
                    }
                }
            }
        },
    }
    return HTMLResponse(json.dumps(asyncapi))
