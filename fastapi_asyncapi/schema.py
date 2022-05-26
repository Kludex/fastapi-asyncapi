import sys
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field, Json

if sys.version_info < (3, 8):
    from typing_extensions import Literal, TypeAlias
elif sys.version_info < (3, 10):
    from typing import Literal

    from typing_extensions import TypeAlias
else:
    from typing import Literal, TypeAlias


def get_supported_scopes(
    flows: Dict[str, Optional[Dict[str, str]]],
) -> List[str]:
    scopes = []
    for key, value in flows.items():
        if value:
            for scope in value["scopes"]:
                scopes.append(scope)
    return scopes


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

    class Config:
        extra = "allow"


class License(BaseModel):
    name: str
    url: Optional[str]

    class Config:
        extra = "allow"


class Info(BaseModel):
    title: str
    version: str
    description: Optional[str]
    termsOfService: Optional[AnyHttpUrl]
    contact: Optional[Contact]
    license: Optional[License]

    class Config:
        extra = "allow"


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
    default: Optional[str]
    description: Optional[str]
    examples: Optional[List[str]]

    class Config:
        extra = "allow"


HTTPMethod = Literal[
    "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "CONNECT", "TRACE"
]

Schema: TypeAlias = Json


class HTTPOperationBinding(BaseModel):
    type: Literal["request", "response"]
    method: HTTPMethod
    query: Optional[Schema] = None
    bindingVersion: Optional[Union[Literal["latest"], str]] = "latest"


class WSOperationBinding(BaseModel):
    method: Literal["GET", "POST"] = "GET"
    query: Optional[Schema] = None
    headers: Optional[Schema] = None
    bindingVersion: Optional[Union[Literal["latest"], str]] = "latest"


class Bindings(BaseModel):
    http: Optional[HTTPOperationBinding] = None
    ws: Optional[WSOperationBinding] = None


class OperationTrait(BaseModel):
    operationId: Optional[str]
    summary: Optional[str]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDocumentation]
    bindings: Bindings


OperationTraits = List[OperationTrait]


class Reference(BaseModel):
    ref: str = Field(..., alias="$ref")


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
    operationId: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[Tag]] = None
    externalDocs: Optional[ExternalDocumentation] = None
    bindings: Optional[Bindings] = None
    traits: Optional[OperationTraits] = None
    message: Optional[Message] = None


Subscribe = Operation
Publish = Operation


class Parameter(BaseModel):
    description: Optional[str]
    _schema: Optional[Schema] = Field(alias="schema")
    location: Optional[str]


Parameters = List[Dict[str, Union[Parameter, Reference]]]


ChannelBindings = Dict[str, Any]


class ChannelItem(BaseModel):
    ref: Optional[str] = Field(default=None, alias="$ref")
    description: Optional[str] = None
    servers: Optional[List[str]] = None
    subscribe: Optional[Subscribe] = None
    publish: Optional[Publish] = None
    parameters: Optional[Parameters] = None
    bindings: Optional[Union[ChannelBindings, Reference]] = None

    # class Config:
    #     allow_population_by_field_name = True


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


class SecuritySchemesType(str, Enum):
    """
    https://www.asyncapi.com/docs/specifications/v2.3.0#securitySchemeObjectType
    """

    USER_PASSWORD = "userPassword"
    API_KEY = "apiKey"
    X509 = "X509"
    SYMMETRIC_ENCRYPTION = "symmetricEncryption"
    ASYMMETRIC_ENCRYPTION = "asymmetricEncryption"
    HTTP_API_KEY = "httpApiKey"
    HTTP = "http"
    OAUTH2 = "oauth2"
    OPENID_CONNECT = "openIdConnect"
    PLAIN = "plain"
    SCRAM_SHA256 = "scramSha256"
    SCRAM_SHA512 = "scramSha512"
    GSSAPI = "gssapi"


class SecurityScheme(BaseModel):
    type: SecuritySchemesType
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
    operationBindings: Optional[Dict[str, Union[Bindings, Reference]]]
    messageBindings: Optional[Dict[str, Union[MessageBinding, Reference]]]

    class Config:
        extra = "allow"


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

    # @root_validator(pre=True)
    # def validate_security(cls, values):
    #     for server_name, server in values.get("servers").items():
    #         for security_req in server["security"]:
    #             cls._validate_security_requirement(security_req, server, values)

    @classmethod
    def _validate_security_requirement(
        cls,
        requirement: SecurityRequirement,
        required_by: str,
        values,
    ) -> None:
        (security_scheme_name, scopes), *other = requirement.items()

        if other:
            raise ValueError(
                f"{required_by} contains invalid "
                f"security requirement: {requirement}"
            )

        security_scheme = cls.__get_security_scheme(values, security_scheme_name)
        if security_scheme is None:
            raise ValueError(
                f"{security_scheme_name} referenced within '{requirement}'"
                " server does not exist in components/securitySchemes"
            )

        if scopes:
            if security_scheme["type"] not in [
                SecuritySchemesType.OAUTH2.value,
                SecuritySchemesType.OPENID_CONNECT.value,
            ]:
                raise ValueError(
                    "Scopes MUST be an empty array for "
                    f"{security_scheme['type']} security requirements"
                )
            check_type = security_scheme["type"] == SecuritySchemesType.OAUTH2.value
            if check_type and security_scheme["flows"]:
                supported_scopes = get_supported_scopes(security_scheme["flows"])

                for scope in scopes:
                    if scope not in supported_scopes:
                        raise ValueError(
                            f"OAuth2 scope {scope} is not defined within "
                            f"the {security_scheme_name} security scheme"
                        )

    @classmethod
    def __get_security_scheme(
        cls,
        values: Dict[str, Any],
        security_scheme_name: str,
    ) -> Optional[Dict[str, Any]]:
        security_scheme = None
        components = values.get("components")
        if components:
            security_schemes = components.get("securitySchemes")
            security_scheme = security_schemes.get(security_scheme_name)
        return security_scheme

    class Config:
        extra = "allow"
