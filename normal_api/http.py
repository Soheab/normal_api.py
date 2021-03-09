import aiohttp


class HTTPSession:
    __slots__ = ("session", "loop")

    def __init__(self):
        self.session = None

    # Aiohttp client sessions must be created in async functions
    async def create_session(self):
        self.session = aiohttp.ClientSession()

    async def request(self, url, *, method = "get", **kwargs):
        if self.session is None:
            await self.create_session()

        return await self.session.request(method, url, **kwargs)

    async def close(self):
        if self.session is not None and not self.session.closed:
            await self.session.close()
            self.session = None
