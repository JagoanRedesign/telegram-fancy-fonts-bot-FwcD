# Fancy Fonts Bot -> Fancy Text, for Telegram Messages
# Last Updated: 02-08-2021

## Imports.
# Telegram (API Wrapper)
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

# Parse JSON
import json

# Custom pseudofonts using unicode.
from pseudofonts import PseudoFont

# Randomization
from uuid import uuid4

## Constants.
# Load the config.json into a 'CONFIG' variable.
with open('config.json') as f:
	CONFIG = json.load(f)

# Load the default fall-back font into a 'FONT_DEFAULT' variable.
with open('fonts/default.json', encoding = 'utf8') as f:
	FONT_DEFAULT = json.load(f)

# Load in all the fonts.
with open('fonts/fonts.json', encoding = 'utf8') as f:
	_FONTS = json.load(f)

# Turn all the font data into pseudofont objects.
FONTS = [
	PseudoFont(
		f['fontName'], 
		f['fontLower'] if f['fontLower'] else FONT_DEFAULT['fontLower'], 
		f['fontUpper'] if f['fontUpper'] else FONT_DEFAULT['fontUpper'], 
		f['fontDigits'] if f['fontDigits'] else FONT_DEFAULT['fontDigits']
	) for f in _FONTS
]

## Info.
print(r"______          _    ______       _   ")
print(r"|  ___|        | |   | ___ \     | |  ")
print(r"| |_ ___  _ __ | |_  | |_/ / ___ | |_ ")
print(r"|  _/ _ \| '_ \| __| | ___ \/ _ \| __|")
print(r"| || (_) | | | | |_  | |_/ / (_) | |_ ")
print(r"\_| \___/|_| |_|\__| \____/ \___/ \__|")  
print(f"{CONFIG['botName']} 1.0.0")
print("~ ", CONFIG['botOwner'], '\n')


## Setup.
print("[Set-Up] Setting up bot..")
updater = Updater(token = CONFIG['botToken'])
dispatcher = updater.dispatcher

## Commands.
def c_start(update: Update, ctx: CallbackContext) -> None:
	"""Info umum tentang bot dan perintah bantuan."""

	text = (
		"Halo! 👋🏻 "
		"Saya adalah bot yang dapat membantu Anda menulis pesan dengan font unicode yang terlihat keren, aneh (dan indah).!\n",
		"⚠️ Beberapa perangkat mungkin tidak mendukung font khusus, jadi ingatlah itu saat Anda mengirim teks penting ke teman.\n",
		"Anda dapat menggunakan saya dengan menyebut saya di obrolan apa pun dan mengetik pesan Anda. Daftar font akan muncul yang dapat Anda pilih."
	)

	ctx.bot.send_message(chat_id = update.effective_chat.id, text = escape_markdown('\n'.join(text), 2), parse_mode = ParseMode.MARKDOWN_V2)

def inlinequery(update: Update, context: CallbackContext) -> None:
	query = update.inline_query.query.strip()
	if not query: return
		
	results = []
	for font in FONTS:
		generated = font(query)
		results.append(
			InlineQueryResultArticle(
				id = uuid4(), 
				title = font.name,
				description = generated,
				input_message_content = InputTextMessageContent(generated)
			)
		)
	update.inline_query.answer(results)

## Command Handler.
print("[Set-Up] Adding handlers..")
# -- Command Handler -- 
dispatcher.add_handler(CommandHandler(('start', 'help'), c_start))

# -- Inline Query Handler --
dispatcher.add_handler(InlineQueryHandler(inlinequery))

## Polling / Login.
updater.start_polling(clean = True)
print("[Ready] Bot is ready. Started polling.")
updater.idle()
