# source: https://github.com/BlistBotList/blist-wrapper/blob/bc0c0fe9afbea39993ccfa8b6d633c2b5be634c8/blist/errors.py
import aiohttp


class NormalAPIException(Exception):
    pass


class BadRequest(NormalAPIException):
    pass


class NotFound(NormalAPIException):
    pass


class InternalServerError(NormalAPIException):
    pass


class Forbidden(NormalAPIException):
    pass


class HTTPException(NormalAPIException):
    def __init__(self, response, message):
        self.response = response
        self.status = response.status
        self.message = message


class _WrapperError:
    def __init__(self, data: dict = None, *, text: str = None) -> None:
        self.status: int = int(data.get("status"))
        self.error: str = str(data.get("error"))
        self.text = text


async def _get_error(response: aiohttp.ClientResponse) -> _WrapperError:
    if response.content_type == "application/json":
        return _WrapperError(await response.json())

    return _WrapperError(text = str(await response.text()))
