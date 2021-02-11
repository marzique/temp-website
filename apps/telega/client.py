import telegram
from telegram.ext import Dispatcher, Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from django.conf import settings


class TelegramBot:
    USER_CHANNEL_ID = settings.TELEGRAM_CHAT_ID  # where messages will be sent
    TECH_CHANNEL_ID = '@tempfc_alerts'

    def __init__(self):
        self.bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

    def send_text(self, text, parse_mode='HTML', chat_id=USER_CHANNEL_ID):
        """Send text message. Text length should be 1-4096 symbols"""

        return self.bot.send_message(
                chat_id=chat_id, 
                text=text, 
                parse_mode=parse_mode
            )

    def send_album(self, photo_urls, caption=None, chat_id=USER_CHANNEL_ID, parse_mode='HTML'):
        """Send 2-10 photos with caption to channel"""

        media_group = [telegram.InputMediaPhoto(url, parse_mode=None) for url in photo_urls]
        media_group[0].caption = caption

        message = self.bot.send_media_group(
            chat_id=chat_id, 
            media=media_group
            )
        return message

bot = TelegramBot()
dispatcher = Dispatcher(bot.bot, None, workers=0)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


# on different commands - answer in Telegram
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))

# on noncommand i.e message - echo the message on Telegram
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
