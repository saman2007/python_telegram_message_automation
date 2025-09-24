import typing


class ErrorResponse(typing.TypedDict):
    code: int
    message: str


class Response(typing.TypedDict):
    error: None | ErrorResponse
    isSuccess: bool


class Account(typing.TypedDict):
    api_id: int
    api_hash: str
    phone_number: str


class MessageDict(typing.TypedDict):
    type: typing.Literal["text", "media"]
    data: typing.Any
