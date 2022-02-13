import pytest
from fastapi.routing import APIRoute

from fastapi_asyncapi.asyncapi import get_asyncapi


def test_get_asyncapi():

    path = '/test/path/'
    title = 'My async api'
    version = "2.3.0"
    routes = [APIRoute(path, lambda x: 1)]
    result = get_asyncapi(title=title, version=version, routes=routes)
    assert result
