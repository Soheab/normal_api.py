# Normal_api.py | Docs

A Python Wrapper for the [Normal API](https://normal-api.ml/)
For any questions and support, you can join the API's server [here](https://discord.gg/FyQ3CnmnQK)

## Getting Started:

To begin with, you'll have to install the package by doing one of the following commands:

- `pip install -U normal_api.py`
- `python -m pip -U install normal_api.py`

After that, you will have to create the client:

```python
import normal_api

normal_api_client = normal_api.Client()
```

For future reference in this documentation: when referring to 'normal_api_client' we refer to that above.

## Using the wrapper:

All available endpoints you can use.

### await normal_api_client.pastebin(text, *, privacy = "public")

Create a public or unlisted pastebin.

#### Parameters

- text ([str]) - Text for the pastebin.
- privacy (Optional[[str]]) - Privacy value for the pastebin, this can only be "public" or "unlisted". Defaults to public.

#### Returns

[Pastebin]

---

### await normal_api_client.imgur(url, *, title = None)

Upload an image to Imgur.

#### Parameters

- url ([str]) - URL of the image to uploader.
- title (Optional[[str]]) - Optional title for the post.

#### Returns

[Imgur]

---

### await normal_api_client.ordinal(number)

https://en.wikipedia.org/wiki/Ordinal_numeral

#### Parameters

- url ([int]) - The number.

#### Returns

[str]

---

### await normal_api_client.user_status(user_id)

Get anyone's status and more.

#### Parameters

- user_id ([int]) - ID of user you want the status of.

#### Returns

[User]

---

### await normal_api_client.invite_info(code)

Get some info on a discord invite.

#### Parameters

- code ([str]) - Invite code.

#### Returns

[Invite]

---

### await normal_api_client.template_info(code)

Get some info on a discord server template.

#### Parameters

- code ([str]) - Template code.

#### Returns

[Template]

--- 

### await normal_api_client.emojify(text)

Convert text to emojis.

#### Parameters

- text ([str]) - Text to convert to emojis.

#### Returns

[Emojified]

--- 

### await normal_api_client.parse_milliseconds(milliseconds)

Parse milliseconds into days,hours, minutes, seconds, milliseconds, microseconds and nanoseconds.

#### Parameters

- milliseconds ([int]) - Milliseconds to parse

#### Returns

[ParsedMS]

--- 

### await normal_api_client.translate(text, *, to_language)

Translate text to x language.

#### Parameters

- text ([str]) - Text to translate
- to_language ([str]) - Language to translate to

#### Returns

[Translated]

--- 

### await normal_api_client.youtube_video_search(query)

Search for a YouTube Video.

#### Parameters

- query ([str]) - Video title to search for

#### Returns

[YoutubeVideo]

---

### await normal_api_client.safe_note(note)

Create a safe that can only be views once.

#### Parameters

- note ([str]) - The secret note

#### Returns

[str] (one time view only url to the safe note)

---

### await normal_api_client.encode(text)

Encode text.

#### Parameters

- text ([str]) - Text to encode

#### Returns

[str]

---

### await normal_api_client.decode(text)

Decode text.

#### Parameters

- text ([str]) - Text to decode

#### Returns

[str]

---

### await normal_api_client.reverse_text(text)

Reverse text.

#### Parameters

- text ([str]) - Text to reverse

#### Returns

[str]

---

### await normal_api_client.image_search(query)

Search for an image related to your text.

#### Parameters

- query ([str]) - Text to search an image for

#### Returns

[Image]

---

### await normal_api_client.random_emoji(category = None, *, nsfw = False)

Get a random emoji from discordemoji.com.

#### Parameters

- category (Optional[[int]]) - Category to search in
- nsfw (Optional[[bool]]) - Determine if the emoji should be NSFW, defaults to False

#### Returns

[RandomEmoji]

---

### await normal_api_client.has_voted_on_topgg(bot_id, user_id, top_gg_token)

Check if user_id has voted on bot_id on top.gg with the bot's token.

#### Parameters

- bot_id ([int]) - Bot ID to check for
- user_id ([int]) - User ID to check for
- top_gg_token ([str]) - Top.gg bot token from here:
  https://top.gg/bot/BOT_ID_HERE/webhooks#:~:text=Token%20for%20this%20bot%3A&text=Show%20token
  the token is sent directly to the top.gg API.

#### Returns

[bool] (True or False)

---

# Objects

Here is explained what attributes the returned objects have

## Image

The object returned from `normal_api_client.image_search()`, `normal_api_client.imgur().image`
, `normal_api_client.random_emoji().image`

#### Image.url

The url of the image

#### await Image.read(bytesio = True)

This will return a [io.BytesIO](https://docs.python.org/3/library/io.html#binary-i-o) object, which can be passed to
discord.File() with a filename for [discord.py](https://github.com/Rapptz/discord.py)

You can set `bytesio` to `False` if you want raw bytes instead of an `io.BytesIO` object.

### str(Image)

The url of the image

---

## Imgur

The object returned from `normal_api_client.imgur()`

#### Imgur.code

The uploaded post's code

#### Imgur.type

The uploaded post's image type. E.g, gif

#### Imgur.image

The uploader image as a [Image] object

#### str(Imgur)

The uploaded post's code

---

## Pastebin

The object returned from `normal_api_client.pastebin()`

#### Pastebin.text

The by you provided text for the post

#### Pastebin.code

The post's code

#### Pastebin.url

The post's URL

#### Pastebin.raw

URL to the raw version of the post

#### Pastebin.privacy_type

Privacy type you chose for the post

#### str(Pastebin)

The post's URL

---

## User

The object returned from `normal_api_client.user_status()`

#### User.username

Username of user

#### User.discriminator

Discriminator of user, without #

#### User.status

The current status of user. E.g, dnd

#### User.activity

Activity info of user, this returns a [User.Activity] object.

#### str(User)

The user's username+#discriminator will be returned

#### int(User)

The user's ID will be returned

---

### User.Activity

The object returned from `normal_api_client.user_status().activity`

#### User.Activity.type

Type of user's activity. E.g, PLAYING

#### User.Activity.text

Status text of user, if available else None

#### User.Activity.emoji

Emoji in status of user, if available else None

#### str(User.Activity)

The user's activity type will be returned, if available

---

## Invite

The object returned from `normal_api_client.invite_info()`

#### Invite.code

Invite code

#### Invite.url

Invite discord.gg URL

#### Invite.inviter

Info on the invite creator, this returns a [Invite.Inviter] object

#### Invite.channel

Info on the invite channel, this returns a [Invite.Channel] object

#### Invite.guild

Info on the invite server, this returns a [Invite.Guild] object

#### str(Invite)

The invite's code will be returned

---

### Invite.Inviter

The object returned from `normal_api_client.invite_info().inviter`

#### Invite.Inviter.username

Username of inviter

#### Invite.Inviter.discriminator

Discriminator of inviter

#### Invite.Inviter.id

ID of inviter

#### str(Invite.Inviter)

The inviters' username+#discriminator will be returned

#### int(Invite.Inviter)

The inviters' id will be returned

---

### Invite.Channel

The object returned from `normal_api_client.invite_info().channel`

#### Invite.Channel.name

Name of channel

#### Invite.Channel.id

ID of channel

#### str(Invite.Channel)

Name of channel

#### int(Invite.Channel)

ID of channel

---

### Invite.Guild

The object returned from `normal_api_client.invite_info().guild`

#### Invite.Guild.name

Name of guild

#### Invite.Guild.id

Description of guild

#### Invite.Guild.id

ID of guild

#### Invite.Guild.members

Total count of members in the guild, if any

#### Invite.Guild.features

Features of guild as a list, if any

#### str(Invite.Guild)

Name of guild the invite was created in will be returned

#### int(Invite.Guild)

ID of guild the invite was created in will be returned

---

## Template

The object returned from `normal_api_client.template_info()`

#### Template.code

Template code

#### Template.description

The guilds' description, if guild has one

#### Template.usage_count

Template usage count

#### Template.roles

All role names in guild as a list, if any

#### Template.channels

All channels (including categories) names in guild as a list, if any

#### Template.creator

Info on the template creator, this returns a [Template.Creator] object

#### Template.guild

Info on the template server, this returns a [Template.Guild] object

#### str(Template)

The template's code will be returned

---

### Template.Creator

The object returned from `normal_api_client.template_info().creator`

#### Template.Creator.username

Username of template creator

#### Template.Creator.discriminator

Discriminator of creator

#### Template.Creator.id

ID of creator

#### str(Template.Creator)

The inviters' username+#discriminator will be returned

#### int(Template.Creator)

The inviters' id will be returned

---

### Template.Guild

The object returned from `normal_api_client.invite_info().guild`

#### Template.Guild.name

Name of guild

#### Template.Guild.id

Description of guild

#### Template.Guild.region

Region of guild

#### Template.Guild.verification_level

Verification level of guild

#### str(Template.Guild)

Name of guild will be returned

#### int(Template.Guild)

ID of guild will be returned

---

## Emojified

The object returned from `normal_api_client.emojify()`

#### Emojified.text

The inputted text

#### Emojified.emojis

Converted text as emojis in single "string"

#### Emojified.emojis_list

Converted text as emojis in ["list", "of", "strings"]

#### str(Emojified)

Same as Emojified.emojis will be returned

---

## ParsedMS

The object returned from `normal_api_client.parse_milliseconds()`

#### ParsedMS.days

Milliseconds to days

#### ParsedMS.hours

Milliseconds to hours

#### ParsedMS.minutes

Milliseconds to minutes

#### ParsedMS.seconds

Milliseconds to seconds

#### ParsedMS.milliseconds

Milliseconds to milliseconds

#### ParsedMS.microseconds

Milliseconds to microseconds

#### ParsedMS.nanoseconds

Milliseconds to nanoseconds

#### int(ParsedMS)

Same as ParsedMS.milliseconds will be returned

#### repr(ParsedMS)

For debug reasons a string of all things will be returned

---

## Translated

The object returned from `normal_api_client.translate()`

#### Translated.text

The inputted text translated to chosen lang

#### Translated.input

The inputted text to translate

#### Translated.translated_to

Lang to translate input to

#### str(Translated)

Same as Translated.text will be returned

---

## YoutubeVideo

The object returned from `normal_api_client.youtube_video_search()`

#### YoutubeVideo.title

Title of returned video

#### YoutubeVideo.description

Description of returned video

#### YoutubeVideo.url

URL of returned video

#### YoutubeVideo.channel_id

Channel ID of returned video uploader

#### str(YoutubeVideo)

Same as YoutubeVideo.url will be returned

---

## RandomEmoji

The object returned from `normal_api_client.random_emoji()`

#### RandomEmoji.name

Name of returned emoji

#### RandomEmoji.description

Category number of returned emoji

#### RandomEmoji.is_nsfw

True or False if emoji is NSFW

#### RandomEmoji.image

Image of emoji as a [Image] object

#### str(RandomEmoji)

Same as RandomEmoji.name will be returned

---

# Examples

##### [invite] info using [discord.py](https://github.com/Rapptz/discord.py):

```python
import discord
import normal_api
from discord.ext import commands

bot = commands.Bot(command_prefix="example.")
normal_api_yes = normal_api.Client() # just a example, the client doesn't have to be under bot

@bot.command()
async def inviteinfo(ctx, code: str): 
    invinfo = await normal_api_yes.invite_info(code)
    my_embed = discord.Embed(
      title = "Invite Info",
      description = f"[Join Server]({invinfo.url})"
    )
    my_embed.add_field(
      name = "Inviter",
      value = f"""
      **Full Name**: {str(invinfo.inviter)}
      **ID**: {invinfo.inviter.id}
      """
    )
    my_embed.add_field(
      name = "Channel",
      value = f"""
      **Full Name**: {invinfo.channel.name}
      **ID**: {invinfo.channel.id}
      """
    )
    my_embed.add_field(
      name = "Server",
      value = f"""
      **Full Name**: {invinfo.guild.name}
      **ID**: {invinfo.guild.id}
      **Features**: {', '.join(invinfo.guild.features) if invinfo.guild.features else 'None'}
      **Total Members**: {invinfo.guild.members}
      """
    )
    await ctx.send(embed=my_embed)
    
# invoke: example.inviteinfo yCzcfju

bot.run("TOKEN")
```

[str]: https://docs.python.org/3/library/stdtypes.html#str
[int]: https://docs.python.org/3/library/functions.html#int
[dict]: https://docs.python.org/3/library/stdtypes.html#dict
[bool]: https://docs.python.org/3/library/functions.html#bool
[tuple]: https://docs.python.org/3/library/stdtypes.html#tuple
[Image]: docs.md#image
[User]: docs.md#user
[Pastebin]: docs.md#pastebin
[Imgur]: docs.md#imgur
[User.Activity]: docs.md#useractivity-1
[Invite]: docs.md#invite
[Invite.Inviter]: docs.md#inviteinviter-1
[Invite.Guild]: docs.md#inviteguild-1
[Invite.Channel]: docs.md#invitechannel-1
[Template]: docs.md#invite
[Template.Creator]: docs.md#templatecreator-1
[Template.Guild]: docs.md#templateguild-1
[Emojified]: docs.md#emojified
[ParsedMS]: docs.md#parsedms
[Translated]: docs.md#translated
[YoutubeVideo]: docs.md#youtubevideo
[RandomEmoji]: docs.md#randomemoji
[invite]: docs.md#await-normal_api_clientinvite_infocode