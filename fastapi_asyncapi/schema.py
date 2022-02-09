from typing import Dict, Optional, List, Literal, Any, Union

from pydantic import BaseModel, AnyHttpUrl, EmailStr, Field

ASYNCAPI_VERSION = '2.0.0'


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
    ref: Optional[str] = Field(alias='$ref')


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


class Channel(BaseModel):
    ref: Optional[str] = Field(alias='$ref')
    description: Optional[str]
    subscribe: Optional[Subscribe]
    publish: Optional[Publish]
    parameters: Optional[Parameters]
    bindings: Optional[Bindings]


Security = Dict[str, List[str]]
Channels = List[Dict[str, Channel]]


class Server(BaseModel):
    url: str
    protocol: Protocol
    protocolVersion: Optional[str]
    description: Optional[str]
    variables: Optional[List[Dict[str, ServerVariable]]]
    security: Optional[List[Security]]
    channels: Channels


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
    _in: str = Field(alias='in')
    scheme: str
    bearerFormat: Optional[str]
    flows: OAUHTFlows
    openIdConnectUrl: str


ServerBinding = Dict[str, Any]

ChannelBinding = Dict[str, Any]


class Components(BaseModel):
    schemas: Optional[Dict[str, Union[Schema, Reference]]]
    messages: Optional[Dict[str, Union[Message, Reference]]]
    securitySchemes: Optional[Dict[str, Union[SecurityScheme, Reference]]]
    parameters: Optional[Dict[str, Union[Parameter, Reference]]]
    correlationIds: Optional[Dict[str, Union[CorrelationID, Reference]]]
    operationTraits: Optional[Dict[str, CorrelationID]]
    messageTraits: Optional[Dict[str, MessageTrait]]
    serverBindings: Optional[Dict[str, ServerBinding]]
    channelBindings: Optional[Dict[str, ChannelBinding]]
    operationBindings: Optional[Dict[str, OperationBinding]]
    messageBindings: Optional[Dict[str, MessageBinding]]


class AsyncAPI(BaseModel):
    asyncapi: str
    id: Optional[str]
    info: Info
    servers: Optional[List[Dict[str, Server]]]
    channels: Optional[Channels]
    components: Optional[Components]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDocumentation]
