import pytest
from faker import Faker
from fastapi.routing import APIRoute

from fastapi_asyncapi.asyncapi import get_asyncapi
from fastapi_asyncapi.schema import AsyncAPI


def test_get_asyncapi():

    path = "/test/path/"
    title = "My async api"
    version = "2.3.0"
    routes = [APIRoute(path, lambda x: 1)]
    result = get_asyncapi(title=title, version=version, routes=routes)
    assert result


def test_asyncapi_spec_validation_invalid_security_requirement_scopes(faker: Faker):
    data = {
        "asyncapi": "2.3.0",
        "info": {
            "title": faker.sentence(),
            "version": faker.pystr(),
            "description": faker.sentence(),
        },
        "channels": {},
        "servers": {
            "development": {
                "url": "localhost",
                "protocol": "ws",
                "security": [{"test": ["a"]}],
            }
        },
        "components": {
            "securitySchemes": {
                "test": {"type": "http", "scheme": "basic"},
                "test2": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
                "testApiKey": {"type": "httpApiKey", "name": "test", "in": "header"},
                "oauth2": {
                    "type": "oauth2",
                    "flows": {
                        "implicit": {
                            "authorizationUrl": "https://localhost:12345",
                            "refreshUrl": "https://localhost:12345/refresh",
                            "scopes": {"a": "A", "b": "B"},
                        }
                    },
                },
            }
        },
    }
    with pytest.raises(ValueError):
        AsyncAPI(**data)


def test_asyncapi_validation_missing_security_scheme(faker: Faker):
    data = {
        "asyncapi": "2.3.0",
        "info": {
            "title": faker.sentence(),
            "version": faker.pystr(),
            "description": faker.sentence(),
        },
        "channels": {},
        "servers": {
            "development": {
                "url": "localhost",
                "protocol": "ws",
                "security": [{"test": []}],
            }
        },
    }
    with pytest.raises(ValueError):
        AsyncAPI(**data)


def test_asyncapi_validation_invalid_security_requirement_undefined_scopes(
    faker: Faker,
):
    data = {
        "asyncapi": "2.3.0",
        "info": {
            "title": faker.sentence(),
            "version": faker.pystr(),
            "description": faker.sentence(),
        },
        "channels": {},
        "servers": {
            "development": {
                "url": "localhost",
                "protocol": "ws",
                "security": [{"oauth2": ["undefined"]}],
            }
        },
        "components": {
            "securitySchemes": {
                "test": {"type": "http", "scheme": "basic"},
                "test2": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
                "testApiKey": {"type": "httpApiKey", "name": "test", "in": "header"},
                "oauth2": {
                    "type": "oauth2",
                    "flows": {
                        "implicit": {
                            "authorizationUrl": "https://localhost:12345",
                            "refreshUrl": "https://localhost:12345/refresh",
                            "scopes": {"a": "A", "b": "B"},
                        }
                    },
                },
            }
        },
    }
    with pytest.raises(ValueError):
        AsyncAPI(**data)
