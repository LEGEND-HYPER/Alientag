import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "__**๐'๐ฆ โก๏ธ ๐๐๐๐๐ ๐๐๐ โก๏ธ**, ๐ข ๐๐๐ง ๐๐๐ง๐ญ๐ข๐จ๐ง ๐๐ฅ๐ฅ ๐๐๐ฆ๐๐๐ซ๐ฌ ๐๐ง ๐๐ซ๐จ๐ฎ๐ฉ ๐ฅ\n๐๐ฅ๐ข๐๐ค **/help** ๐๐จ๐ซ ๐๐จ๐ซ๐ ๐๐ง๐๐จ๐ซ๐ฆ๐๐ญ๐ข๐จ๐ง__\n\n ๐๐จ๐ฅ๐ฅ๐จ๐ฐ [๐๐๐๐๐ ๐](https://t.me/ALIEN_X_SUPPORT) ๐ข๐ป ๐๐๐ฅ๐๐๐ซ๐๐ฆ",
    link_preview=False,
    buttons=(
      [
        Button.url('โ๐๐๐๐๐๐๐๐ ', 'https://t.me/ALIEN_X_SUPPORT'),
        Button.url('โก๏ธ๐๐๐ ๐๐โก๏ธ', 'https://t.me/ALIEN_MENTION_ROBOT?startgroup=true'),
        Button.url('๐งฉ สแดสแด แดษดแด แดแดแดแดแดษดแด๊ฑ ๐', 'https://telegra.ph/ALIEN-MENTION-ROBOT-COMMANDS-01-25-2')  
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Help Menu of TagAllBot**\n\nCommand: /all\n__You can use this command with text what you want to mention others.__\nExample: `/all Good Morning!`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\n\nFollow [๐๐๐๐๐ ๐](https://t.me/ALIEN_X_SUPPORT) ๐ข๐ก ๐ง๐๐๐๐๐ฅ๐๐ "
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
     [
        Button.url('โ๐๐๐๐๐๐๐๐ ', 'https://t.me/ALIEN_X_SUPPORT'),
        Button.url('โก๏ธ๐๐๐ ๐๐โก๏ธ', 'https://t.me/ALIEN_MENTION_ROBOT?startgroup=true'),
        Button.url('๐งฉ สแดสแด แดษดแด แดแดแดแดแดษดแด๊ฑ ๐', 'https://telegra.ph/ALIEN-MENTION-ROBOT-COMMANDS-01-25-2')  
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def all(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command Can Be Use In Groups And Channels @ALIEN_X_SUPPORT !__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only Admins Can Mention All\n\nFor More Go On @ALIEN_X_SUPPORT !__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I Can't Mention Members For Older Messages! (messages which are sent before I'm added to group)__")
  else:
    return await event.respond("__Reply To a Message Or Give Me Some Text To Mention Others\n\nMade by @ALIEN_X_SUPPORT !__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}\n\nMade by [๐๐๐๐๐๐](https://t.me/ABOUT_MUKUND) โ๏ธ๐ฅ"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There Is No Proccess On Going @ALIEN_X_SUPPORT...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')

print(">> HACKER TAGALL STARTED @ALIEN_X_SUPPORT<<")
client.run_until_disconnected()
