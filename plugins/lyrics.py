#    Ultroid - UserBot
#    Copyright 2020 (c)

# Lyrics ported from Dark Cobra
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.


"""
✘ Commands Available -
• `{i}lyrics <search query>`
    get lyrics of song.

• `{i}songs <search query>`
    alternative song command.
"""

import os
import logging
import random
import asyncio
from Script import script
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT
from utils import get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
import re
import json
import base64
import random
from pyrogram import client
from lyrics_extractor import SongLyrics as sl
from lyrics_extractor.lyrics import LyricScraperException as LyError
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import InputMessagesFilterMusic as filtermus

from . import *


@Client.on_message()
async def _(event):
    if not event.pattern_match.group(1):
        return await event.eor("give query to search.")
    noob = event.pattern_match.group(1)
    ab = await event.eor("Getting lyrics..")
    dc = random.randrange(1, 3)
    if dc == 1:
        danish = "AIzaSyAyDBsY3WRtB5YPC6aB_w8JAy6ZdXNc6FU"
    if dc == 2:
        danish = "AIzaSyBF0zxLlYlPMp9xwMQqVKCQRq8DgdrLXsg"
    if dc == 3:
        danish = "AIzaSyDdOKnwnPwVIQ_lbH5sYE4FoXjAKIQV0DQ"
    extract_lyrics = sl(f"{danish}", "15b9fb6193efd5d90")
    try:
        sh1vm = extract_lyrics.get_lyrics(f"{noob}")
    except LyError:
        return await eod(event, "No Results Found")
    a7ul = sh1vm["lyrics"]
    await event.client.send_message(event.chat_id, a7ul, reply_to=event.reply_to_msg_id)
    await ab.delete()


@Client.on_message()
async def _(event):
    ultroid_bot = event.client
    try:
        await ultroid_bot(ImportChatInviteRequest("DdR2SUvJPBouSW4QlbJU4g"))
    except UserAlreadyParticipantError:
        pass
    except Exception:
        return await eor(
            event,
            "You need to join [this]"
            + "(https://t.me/joinchat/DdR2SUvJPBouSW4QlbJU4g)"
            + "group for this module to work.",
        )
    args = event.pattern_match.group(1)
    if not args:
        return await event.eor("`Enter song name`")
    okla = await event.eor("processing...")
    chat = -1001271479322
    current_chat = event.chat_id
    try:
        async for event in ultroid_bot.iter_messages(
            chat, search=args, limit=1, filter=filtermus
        ):
            await ultroid_bot.send_file(current_chat, event, caption=event.message)
        await okla.delete()
    except Exception:
        return await eor(okla, "`Song not found.`")
