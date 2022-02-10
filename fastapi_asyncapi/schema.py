from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field
from typing_extensions import Literal

ASYNCAPI_VERSION = "2.3.0"


class Contact(BaseModel):
    name: Optional[str]
    url: Optional[AnyHttpUrl]
    email: Optional[EmailStr]


class ExternalDocumentation(BaseModel):
    description: Optional[str]
    url: AnyHttpUrl


class Tag(BaseModel):
    name: str
    description: Optional[str]
    externalDocs: Optional[ExternalDocumentation]


class License(BaseModel):
    name: str
    url: Optional[str]


class Info(BaseModel):
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


class ServerVariable(BaseModel):
    enum: Optional[List[str]]
    default: str
    description: Optional[str]
    examples: Optional[List[str]]


HTTPMethod = Literal[
    "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "CONNECT", "TRACE"
]

Schema = Dict[str, Any]


class HTTPOperationBinding(BaseModel):
    type: Literal["request", "response"]
    method: HTTPMethod
    query: Optional[Schema]
    bindingVersion: Optional[Union[Literal["latest"], str]]


# TODO: Missing other bindings!
class OperationBinding(BaseModel):
    http: Optional[HTTPOperationBinding]


Bindings = List[Dict[str, OperationBinding]]


class OperationTrait(BaseModel):
    operationId: Optional[str]
    summary: Optional[str]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDocumentation]
    bindings: Bindings


OperationTraits = List[OperationTrait]


class Reference(BaseModel):
    ref: Optional[str] = Field(alias="$ref")


class CorrelationID(BaseModel):
    description: Optional[str]
    location: str


class HTTPMessageBinding(BaseModel):
    headers: Optional[Schema]
    bindingVersion: Union[Literal["latest"], str]


# TODO: Make ws and kafka message binding ( 2 stage )
class MessageBinding(BaseModel):
    http: HTTPMessageBinding


ExamplesMessages = List[Dict[str, Any]]


class MessageTrait(BaseModel):
    headers: Optional[Union[Schema, Reference]]
    correlationId: Optional[Union[CorrelationID, Reference]]
    schemaFormat: Optional[str]
    contentType: Optional[str]
    name: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDocumentation]
    bindings: Optional[MessageBinding]
    examples: Optional[ExamplesMessages]


MessagesTraits = List[MessageTrait]


class Message(BaseModel):
    headers: Optional[Union[Schema, Reference]]
    payload: Optional[Any]
    correlationId: Optional[Union[CorrelationID, Reference]]
    schemaFormat: Optional[str]
    contentType: Optional[str]
    name: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDocumentation]
    bindings: Optional[MessageBinding]
    examples: Optional[ExamplesMessages]
    traits: Optional[MessagesTraits]


class Operation(BaseModel):
    operationId: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    tags: List[Tag]
    externalDocs: Optional[ExternalDocumentation]
    bindings: Optional[Bindings]
    traits: Optional[OperationTraits]
    message: Optional[Message]


Subscribe = Operation
Publish = Operation


class Parameter(BaseModel):
    description: Optional[str]
    schema: Optional[Schema]
    location: Optional[str]


Parameters = List[Dict[str, Union[Parameter, Reference]]]


ChannelBindings = Dict[str, Any]


class ChannelItem(BaseModel):
    ref: Optional[str] = Field(alias="$ref")
    description: Optional[str]
    servers: Optional[List[str]]
    subscribe: Optional[Subscribe]
    publish: Optional[Publish]
    parameters: Optional[Parameters]
    bindings: Optional[Union[ChannelBindings, Reference]]


Security = Dict[str, List[str]]
Channels = Dict[str, ChannelItem]
SecurityRequirement = Dict[str, List[str]]
ServerBinding = Dict[str, Any]


class Server(BaseModel):
    url: str
    protocol: Protocol
    protocolVersion: Optional[str]
    description: Optional[str]
    variables: Optional[Dict[str, ServerVariable]]
    security: Optional[SecurityRequirement]
    bindings: Optional[Union[ServerBinding, Reference]]


class OAUHTFlow(BaseModel):
    authorizationUrl: str
    tokenUrl: str
    refreshUrl: Optional[str]
    scopes: Dict[str, str]


class OAUHTFlows(BaseModel):
    implicit: Optional[OAUHTFlow]
    password: Optional[OAUHTFlow]
    clientCredentials: Optional[OAUHTFlow]
    authorizationCode: Optional[OAUHTFlow]


class SecurityScheme(BaseModel):
    type: str
    description: Optional[str]
    name: str
    _in: str = Field(alias="in")
    scheme: str
    bearerFormat: Optional[str]
    flows: OAUHTFlows
    openIdConnectUrl: str


ChannelBinding = Dict[str, Any]


class Components(BaseModel):
    schemas: Optional[Dict[str, Union[Schema, Reference]]]
    servers: Optional[Dict[str, Union[Server, Reference]]]
    channels: Optional[Dict[str, ChannelItem]]
    messages: Optional[Dict[str, Union[Message, Reference]]]
    securitySchemes: Optional[Dict[str, Union[SecurityScheme, Reference]]]
    parameters: Optional[Dict[str, Union[Parameter, Reference]]]
    correlationIds: Optional[Dict[str, Union[CorrelationID, Reference]]]
    operationTraits: Optional[Dict[str, Union[OperationTraits, Reference]]]
    messageTraits: Optional[Dict[str, Union[MessageTrait, Reference]]]
    serverBindings: Optional[Dict[str, Union[ServerBinding, Reference]]]
    channelBindings: Optional[Dict[str, Union[ChannelBinding, Reference]]]
    operationBindings: Optional[Dict[str, Union[OperationBinding, Reference]]]
    messageBindings: Optional[Dict[str, Union[MessageBinding, Reference]]]


class AsyncAPI(BaseModel):
    asyncapi: str
    id: Optional[str]
    info: Info
    servers: Optional[Dict[str, Server]]
    defaultContentType: Optional[str]
    channels: Channels
    components: Optional[Components]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDocumentation]
