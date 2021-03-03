from asyncio import AbstractEventLoop, get_event_loop
from urllib.parse import quote, urlencode
from aiohttp import ClientSession
from .classes import (Template, Emojified, Image, Imgur, Invite, ParsedMS, RandomEmoji, SafeNote,
                      Translated, User, YoutubeVideo, Pastebin)
from .errors import BadRequest, Forbidden, HTTPException, InternalServerError, NotFound


class Client:
    __slots__ = ("token", "session", "loop", "_api_url")

    def __init__(self, *, session: ClientSession = None, loop: AbstractEventLoop = None) -> None:
        self.session = ClientSession(loop = get_event_loop() or loop) or session
        self._api_url = "https://normal-api.ml/"

    async def _api_request(self, endpoint: str, params: dict = None, *, not_json: bool = False):
        url = f"{self._api_url}{endpoint}"
        if params:
            encoded_param = urlencode(params, quote_via = quote)
            url += f"?{encoded_param}"
        response = await self.session.get(str(url))

        if response.status == 200:
            if str(response.content_type) == "application/json" and not not_json:
                return await response.json()
            return response
        elif response.status == 400:
            raise BadRequest((await response.json()).get("error", None))
        elif response.status == 403:
            raise Forbidden((await response.json()).get("error", None))
        elif response.status == 404:
            raise NotFound((await response.json()).get("error", None))
        elif response.status == 500:
            raise InternalServerError((await response.json()).get("error", None))
        else:
            raise HTTPException(response, str(await response.text()))

    async def pastebin(self, text: str, privacy: str) -> Pastebin:
        VALID_PRIVACY_VALUES = ["public", "unlisted"]
        if str(privacy) not in VALID_PRIVACY_VALUES:
            raise Forbidden(f"Invalid Privacy Value. Valid values: {', '.join(VALID_PRIVACY_VALUES)}")
        response = await self._api_request("pastebin", {"text": str(text), "privacy": str(privacy)})

        return Pastebin(response, str(privacy))

    async def imgur(self, url: str, title: str = None) -> Imgur:
        params = {"url": url}
        if title:
            params['title'] = str(title)

        response = await self._api_request("imgur", params)
        image = await self.session.get(response['url'])

        return Imgur(image, response)

    async def ordinal(self, number: int) -> str:
        response = await self._api_request("ordinal", {"num": int(number)})
        return response['ordinal']

    async def user_status(self, user_id: int) -> User:
        response = await self._api_request("userstatus", {"userid": int(user_id)})
        return User(response)

    async def invite_info(self, code: str) -> Invite:
        response = await self._api_request("inviteinfo", {"code": str(code)})
        return Invite(response)

    async def template_info(self, code: str) -> Template:
        response = await self._api_request("templateinfo", {"code": str(code)})
        return Template(response)

    async def emojify(self, text: str) -> Emojified:
        response = await self._api_request("emojify", {"text": str(text)})
        return Emojified(response)

    async def parse_milliseconds(self, milliseconds: int) -> ParsedMS:
        response = await self._api_request("parsems", {"ms": int(milliseconds)})
        return ParsedMS(response)

    async def translate(self, text: str, to_language: str) -> Translated:
        response = await self._api_request("translate", {"text": str(text), "to": str(to_language)})
        return Translated(response)

    async def youtube_video_search(self, query: str) -> YoutubeVideo:
        response = await self._api_request("youtube/searchvideo", {"query": str(query)})
        return YoutubeVideo(response)

    async def safe_note(self, note: str) -> SafeNote:
        response = await self._api_request("safenote", {"note": str(note)})
        return response['url']

    async def encode(self, text: str) -> str:
        response = await self._api_request("encode", {"text": str(text)})
        return response['encoded']

    async def decode(self, text: str) -> str:
        response = await self._api_request("decode", {"text": str(text)})
        return response['decoded']

    async def reverse_text(self, text: str) -> str:
        response = await self._api_request("reverse", {"text": str(text)})
        return response['reversed']

    async def image_search(self, query: str) -> Image:
        response = await self._api_request("image-search", {"query": str(query)})
        image_response = await self.session.get(response['image'])
        return Image(str(image_response.url), image_response)

    async def random_emoji(self, category: int = None, nsfw: bool = False) -> RandomEmoji:
        params = {}
        if category:
            params["category"] = int(category)
        if category:
            params["nsfw"] = True
        response = await self._api_request("randomemoji", params)
        params = dict(response)
        params['nsfw'] = nsfw
        image_response = await self.session.get(response['image'])
        return RandomEmoji(image_response, params)

    async def has_voted_on_topgg(self, bot_id: int, user_id: int, top_gg_token: str) -> bool:
        response = await self._api_request("topgg/hasvoted", {"bot": int(bot_id), "user": int(user_id),
                                                              "token": str(top_gg_token)})
        has_voted = response['voted']
        return True if str(has_voted) == "true" else False

    # Session

    async def close(self) -> None:
        if not self.session.closed:
            await self.session.close()
