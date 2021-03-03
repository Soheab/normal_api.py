# source: https://github.com/BlistBotList/blist-wrapper/blob/bc0c0fe9afbea39993ccfa8b6d633c2b5be634c8/blist/errors.py


class CoolImagesException(Exception):
    pass


class BadRequest(CoolImagesException):
    pass


class NotFound(CoolImagesException):
    pass


class InternalServerError(CoolImagesException):
    pass


class Forbidden(CoolImagesException):
    pass


class HTTPException(CoolImagesException):
    def __init__(self, response, message):
        self.response = response
        self.status = response.status
        self.message = message
