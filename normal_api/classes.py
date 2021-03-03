from enum import Enum
from io import BytesIO
from typing import Union, Optional

import typing

from aiohttp import ClientResponse, ClientSession


def UNDEFINED_OR_NULL(text: Union[str, int], integer = False):
    if str(text) in ["undefined", "null"]:
        return None

    return str(text) if not integer else int(text)


class Image:
    def __init__(self, url: str, response: ClientResponse) -> None:
        self.url: str = url
        self.response: ClientResponse = response

    def __str__(self) -> str:
        return self.url if self.url is not None else ""

    async def read(self, bytesio = True) -> Union[bytes, BytesIO]:
        _bytes = await self.response.read()
        if bytesio is False:
            return _bytes

        return BytesIO(_bytes)


class Pastebin:
    def __init__(self, data: dict, privacy_type: str) -> None:
        self.code: str = data.get("code")
        self.url: str = data.get("url")
        self.raw: str = data.get("raw")
        self.text: str = data.get("text")
        self.privacy_type: str = str(privacy_type)

    def __str__(self):
        return self.url


class Imgur:
    def __init__(self, image_response: ClientResponse, data: dict) -> None:
        self._image_response: ClientResponse = image_response
        self.code: str = data.get("code")
        self.type: str = data.get("type")

    def __str__(self):
        return self.code

    @property
    def image(self):
        return Image(str(self._image_response.url), self._image_response)


class User:
    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.username: str = data.get("username")
        self.discriminator: int = int(data.get("discrim"))
        self.id: int = int(data.get("id"))
        self.status: Optional[str] = UNDEFINED_OR_NULL(data.get("user_status", None))
        self.activity: User.Activity = User.Activity(data.get(data))

    def __str__(self):
        return str(self._data['tag'])

    def __int__(self):
        return int(self._data['id'])

    class Activity:
        def __init__(self, data: dict) -> None:
            self.type: Optional[str] = UNDEFINED_OR_NULL(data.get("status_type"))
            self.text: Optional[str] = UNDEFINED_OR_NULL(data.get("custom_status"))
            self.emoji: Optional[str] = UNDEFINED_OR_NULL(data.get("custom_status_emoji"))

        def __str__(self):
            return str(self.type) if self.type else ''


class Invite:
    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.code: str = data.get("code")
        self.url: str = data.get("url")
        self.inviter: Invite.Inviter = Invite.Inviter(self._data)
        self.channel: Invite.Channel = Invite.Channel(self._data)
        self.guild: Invite.Guild = Invite.Guild(self._data)

    def __str__(self):
        return self.code

    class Inviter:
        def __init__(self, data: dict) -> None:
            self._data: dict = data
            self._tag: str = data.get("inviter_tag")
            self.__split_tag: list = self._tag.split("#")
            self.username: str = self.__split_tag[0]
            self.discriminator: str = self.__split_tag[1]
            self.id: int = int(data.get("inviter_id"))

        def __str__(self):
            return self._tag if self._tag else ''

        def __int__(self):
            return self.id

    class Guild:
        def __init__(self, data: dict) -> None:
            self._data: dict = data
            self.name: str = data.get("guild_name")
            self.members: Optional[int] = UNDEFINED_OR_NULL(data.get("guild_members"), True)
            self.id: int = int(data.get("guild_id"))
            self.description: Optional[str] = UNDEFINED_OR_NULL(data.get("guild_description"))

        def features(self) -> Optional[list]:
            features_string = UNDEFINED_OR_NULL(self._data.get("guild_features"))
            if features_string:
                return features_string.strip().split(",")
            return features_string

        def __str__(self):
            return self.name

        def __int__(self):
            return self.id

    class Channel:
        def __init__(self, data: dict) -> None:
            self._data: dict = data
            self.name: str = data.get("channel_name")
            self.id: int = int(data.get("channel_id"))

        def __str__(self):
            return self.name

        def __int__(self):
            return self.id


class Template:
    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.code: str = data.get("code")
        self.url: str = data.get("url")
        self.description: str = UNDEFINED_OR_NULL(data.get("description"))
        self.usage_count: int = int(data.get("usage_count"))
        self.creator: Template.Creator = Template.Creator(self._data)
        self.guild: Template.Guild = Template.Guild(self._data)

    def roles(self) -> Optional[list]:
        roles_string = UNDEFINED_OR_NULL(self._data.get("roles"))
        if roles_string:
            return roles_string.strip().split(",")
        return roles_string

    def channels(self) -> Optional[list]:
        channels_string = UNDEFINED_OR_NULL(self._data.get("channels"))
        if channels_string:
            return channels_string.strip().split(",")
        return channels_string

    def __str__(self):
        return str(self._data['code'])

    class Creator:
        def __init__(self, data: dict) -> None:
            self._data: dict = data
            self._creator_tag: str = data.get("creator_tag")
            self.__split_creator_tag: list = self._creator_tag.split("#")
            self.username: str = self.__split_creator_tag[0]
            self.discriminator: str = self.__split_creator_tag[1]
            self.id: int = int(data.get("creator_id"))

        def __str__(self):
            return self._creator_tag if self._creator_tag else ''

        def __int__(self):
            return self.id

    class Guild:
        def __init__(self, data: dict) -> None:
            self._data: dict = data
            self.name: str = data.get("guild_name")
            self.id: int = int(data.get("guild_id"))
            self.region: str = data.get("guild_region")
            self.verification_level: int = int(data.get("guild_verification_level"))

        def __str__(self):
            return self.name

        def __int__(self):
            return self.id


class Emojified:
    def __init__(self, data: dict) -> None:
        self.text: str = data.get("text")
        self.emojis: str = data.get("emojify")
        self.emojis_list: list = self.emojis.split(" ")

    def __str__(self):
        return str(self.emojis)


class ParsedMS:
    def __init__(self, data: dict) -> None:
        self.days: int = int(data.get("days"))
        self.hours: int = int(data.get("hours"))
        self.minutes: int = int(data.get("minutes"))
        self.seconds: int = int(data.get("seconds"))
        self.milliseconds: int = int(data.get("milliseconds"))
        self.microseconds: int = int(data.get("microseconds"))
        self.nanoseconds: int = int(data.get("nanoseconds"))

    def __repr__(self):
        return "<ParsedMS {0.days}, {0.hours}, {0.minutes}, {0.seconds}, {0.milliseconds}, {0.microseconds}, " \
               "{0.nanoseconds}>".format(self)

    def __int__(self):
        return self.microseconds


class Translated:
    def __init__(self, data: dict) -> None:
        self.input: str = data.get("text")
        self.text: str = data.get("translated")
        self.translated_to: str = data.get("translatedTo")

    def __str__(self):
        return str(self.text)


class YoutubeVideo:
    def __init__(self, data: dict) -> None:
        self.title: str = data.get("title")
        self.description: str = data.get("description")
        self.url: str = data.get("url")
        self.channel_id: str = data.get("channel_id")

    def __str__(self):
        return str(self.url)


class RandomEmoji:
    def __init__(self, image_response: ClientResponse, data: dict) -> None:
        self._image_response: ClientResponse = image_response
        self.name: str = data.get("title")
        self.category: int = int(data.get("category"))
        self.is_nsfw: str = data.get("nsfw")

    def __str__(self):
        return self.name

    @property
    def image(self):
        return Image(str(self._image_response.url), self._image_response)
