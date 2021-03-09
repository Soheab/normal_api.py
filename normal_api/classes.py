from io import BytesIO
from typing import Optional, Union

from aiohttp import ClientResponse


def _UNDEFINED_OR_NULL(text: Union[str, int], integer = False):
    if str(text) in ["undefined", "null"]:
        return None

    return str(text) if not integer else int(text)


class Image:
    def __init__(self, url: str, response: ClientResponse) -> None:
        self.url: str = url
        self._response: ClientResponse = response

    def __str__(self) -> str:
        return self.url if self.url is not None else ""

    def __repr__(self):
        return "<Image url={0.url}>".format(self)

    async def read(self, bytesio = True) -> Union[bytes, BytesIO]:
        _bytes = await self._response.read()
        if bytesio is False:
            return _bytes

        return BytesIO(_bytes)


class Pastebin:
    def __init__(self, data: dict) -> None:
        self.code: str = data.get("code")
        self.url: str = data.get("url")
        self.raw: str = data.get("raw")
        self.text: str = data.get("text")
        self.privacy_type: str = data.get("privacy")

    def __str__(self):
        return self.url

    def __repr__(self):
        return "<Pastebin code={0.code} url={0.url} raw={0.raw} text={0.text} " \
               "privacy_type={0.privacy_type}>".format(self)


class Imgur:
    def __init__(self, image_response: ClientResponse, data: dict) -> None:
        self._image_response: ClientResponse = image_response
        self.code: str = data.get("code")
        self.type: str = data.get("type")

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<Imgur code={0.code} type={0.type} image={0.image!r}>".format(self)

    @property
    def image(self):
        return Image(str(self._image_response.url), self._image_response)


class User:

    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.username: str = data.get("username")
        self.status: Optional[str] = _UNDEFINED_OR_NULL(data.get("user_status", None))
        self.activity: User.Activity = User.Activity(data)

    @property
    def id(self):
        _id = _UNDEFINED_OR_NULL(self._data.get("id"))
        if _id:
            return int(_id)
        return _id

    @property
    def discriminator(self):
        discrim = _UNDEFINED_OR_NULL(self._data.get("discrim"))
        if discrim:
            return int(discrim)
        return discrim

    def __repr__(self):
        return "<User username={0.username} id={0.id} discriminator={0.discriminator}" \
               " status={0.status} activity={0.activity!r}>".format(self)

    def __str__(self):
        return str(self._data['tag'])

    def __int__(self):
        return int(self._data['id'])

    class Activity:
        def __init__(self, data: dict) -> None:
            self.type: Optional[str] = _UNDEFINED_OR_NULL(data.get("status_type"))
            self.text: Optional[str] = _UNDEFINED_OR_NULL(data.get("custom_status"))
            self.emoji: Optional[str] = _UNDEFINED_OR_NULL(data.get("custom_status_emoji"))

        def __repr__(self):
            return "<Activity type={0.type} text={0.text} emoji={0.emoji}>".format(self)

        def __str__(self):
            return str(self.type) if self.type else ''


class Invite:
    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.code: str = data.get("code")
        self.url: str = data.get("url")
        self.inviter: Invite.Inviter = Invite.Inviter(self._data)
        self.guild: Invite.Guild = Invite.Guild(self._data)
        self.channel: Invite.Channel = Invite.Channel(self._data)

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<Invite code={0.code} url={0.url} inviter={0.inviter!r} " \
               "guild={0.guild!r} channel={0.channel!r}>".format(self)

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

        def __repr__(self):
            return "<Inviter username={0.username} discriminator={0.discriminator} id={0.id}>".format(self)

    class Guild:
        def __init__(self, data: dict) -> None:
            self._data: dict = data
            self.name: str = data.get("guild_name")
            self.members: Optional[int] = _UNDEFINED_OR_NULL(data.get("guild_members", 0), True)
            self.id: int = int(data.get("guild_id"))
            self.description: Optional[str] = _UNDEFINED_OR_NULL(data.get("guild_description"))

        @property
        def features(self) -> Optional[list]:
            features_string = _UNDEFINED_OR_NULL(self._data.get("guild_features"))
            if features_string:
                return features_string.strip().split(",")
            return []

        def __str__(self):
            return self.name

        def __int__(self):
            return self.id

        def __repr__(self):
            return "<Guild name={0.name} id={0.id} description={0.description} " \
                   "members={0.members} features={0.features}>".format(self)

    class Channel:
        def __init__(self, data: dict) -> None:
            self._data: dict = data
            self.name: str = data.get("channel_name")
            self.id: int = int(data.get("channel_id"))

        def __str__(self):
            return self.name

        def __int__(self):
            return self.id

        def __repr__(self):
            return "<Channel name={0.name} id={0.id}>".format(self)


class Template:
    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.code: str = data.get("code")
        self.url: str = data.get("url")
        self.description: str = _UNDEFINED_OR_NULL(data.get("description"))
        self.usage_count: int = int(data.get("usage_count"))
        self.creator: Template.Creator = Template.Creator(self._data)
        self.guild: Template.Guild = Template.Guild(self._data)

    @property
    def roles(self) -> Optional[list]:
        roles_string = _UNDEFINED_OR_NULL(self._data.get("roles"))
        if roles_string:
            return roles_string.strip().split(",")
        return []

    @property
    def channels(self) -> Optional[list]:
        channels_string = _UNDEFINED_OR_NULL(self._data.get("channels"))
        if channels_string:
            return channels_string.strip().split(",")
        return []

    def __str__(self):
        return str(self._data['code'])

    def __repr__(self):
        return "<Template code={0.code} url={0.url} description={0.description} " \
               "usage_count={0.usage_count} roles={0.roles} channels={0.channels} " \
               "creator={0.creator!r} guild={0.guild!r}>".format(self)

    class Creator:
        def __init__(self, data: dict) -> None:
            self._data: dict = data
            self._creator_tag: str = data.get("creator_tag")
            self.__split_creator_tag: list = self._creator_tag.split("#")
            self.username: str = self.__split_creator_tag[0]
            self.id: int = int(data.get("creator_id"))
            self.discriminator: str = self.__split_creator_tag[1]

        def __str__(self):
            return self._creator_tag if self._creator_tag else ''

        def __int__(self):
            return self.id

        def __repr__(self):
            return "<Creator username={0.username} id={0.id} discriminator={0.discriminator}>".format(self)

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

        def __repr__(self):
            return "<Guild name={0.name} id={0.id} region={0.region} " \
                   "verification_level={0.verification_level}>".format(self)


class Emojified:
    def __init__(self, data: dict) -> None:
        self.text: str = data.get("text")
        self.emojis: str = data.get("emojify")
        self.emojis_list: list = self.emojis.split(" ")

    def __str__(self):
        return str(self.emojis)

    def __repr__(self):
        return "<Emojified text={0.text} emojis={0.emojis} emojis_list={0.emojis_list}>".format(self)


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
        return "<ParsedMS days={0.days} hours={0.hours} minutes={0.minutes} seconds={0.seconds} " \
               "milliseconds={0.milliseconds} microseconds={0.microseconds} nanoseconds={0.nanoseconds}>".format(self)

    def __int__(self):
        return self.microseconds


class Translated:
    def __init__(self, data: dict) -> None:
        self.input: str = data.get("text")
        self.text: str = data.get("translated")
        self.translated_to: str = data.get("translatedTo")

    def __str__(self):
        return str(self.text)

    def __repr__(self):
        return "<Translated input={0.input} text={0.text} translated_to={0.translated_to}>".format(self)


class YoutubeVideo:
    def __init__(self, data: dict) -> None:
        self.title: str = data.get("title")
        self.description: str = data.get("description")
        self.url: str = data.get("url")
        self.channel_id: str = data.get("channel_id")

    def __str__(self):
        return str(self.url)

    def __repr__(self):
        return "<YoutubeVideo title={0.title} description={0.description} " \
               "url={0.url} channel_id={0.channel_id}>".format(self)


class RandomEmoji:
    def __init__(self, image_response: ClientResponse, data: dict) -> None:
        self._image_response: ClientResponse = image_response
        self.name: str = data.get("title")
        self.category: int = int(data.get("category"))
        self.is_nsfw: bool = data.get("nsfw")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<RandomEmoji name={0.name} category={0.category} is_nsfw={0.is_nsfw} image={0.image!r}>".format(self)

    @property
    def image(self):
        return Image(str(self._image_response.url), self._image_response)
