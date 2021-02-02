import telegram

from django.conf import settings


class TelegramBot:
    CHANNEL_ID = settings.TELEGRAM_CHAT_ID  # where messages will be sent

    def __init__(self):
        self.bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

    def send_text(self, text, parse_mode='HTML'):
        """Send text message. Text length should be 1-4096 symbols"""

        return self.bot.send_message(
                chat_id=self.CHANNEL_ID, 
                text=text, 
                parse_mode=parse_mode
            )

    def send_album(self, photo_urls, caption=None):
        """Send 2-10 photos with caption to channel"""

        media_group = [telegram.InputMediaPhoto(url, parse_mode=None) for url in photo_urls]
        media_group[0].caption = caption

        message = self.bot.send_media_group(
            chat_id=self.CHANNEL_ID, 
            media=media_group
            )
        return message
