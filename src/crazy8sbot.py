import requests
import constants as const
from telegram.ext import * #should be different
import conversation_handler as ch

global requestURL
requestURL = "http://api.telegram.org/bot" + const.BOT_TOKEN + "/getUpdates"

update_str = requests.get(requestURL)
print(requests.get(requestURL).json())


def start_command(update, context):
    update.message.reply_text('ya, watyawant')

def help_command(update, context):
    update.message.reply_text('ya, help')

def message_handler(update, conext):
    text = str(update.message.text).lower
    response = ch.reply(text)
    update.messafe.reply_text(response)