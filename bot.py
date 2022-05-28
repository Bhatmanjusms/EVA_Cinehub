import logging
import logging.config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR
from utils import temp
from user import user

class Bot(Client):
    USER: user = None
    USER_ID: int = None

    def __init__(self):
        super().__init__(
            SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        btn = [
        [
            InlineKeyboardButton('⚡️ ℂ𝕀ℕ𝔼𝕄𝔸 ℍ𝕌𝔹 ⚡️', url=f'https://t.me/cinemahub02')
        ]
        ]
        await self.USER.send_message(
            chat_id=-1001308633613,
            text="🧭🧭 <b>GROUP OPENED</b> 🧭🧭\n\n✅ Requests are allowed, Let's start.\n\n🌄 Good morning.", reply_markup=InlineKeyboardMarkup(btn)
        )
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with Pyrogram v{__version__} (Layer {layer}) started.")
        logging.info(LOG_STR)

    async def stop(self, *args):
        await super().stop()
        await self.send_message(
            chat_id=-1001308633613,
            text="🧭🧭 <b>GROUP CLOSED</b> 🧭🧭\n\n✅ Requests are allowed, Let's start.\n\n🌄 Good morning."
        )
        logging.info("Bot stopped. Bye.")


app = Bot()
app.run()
