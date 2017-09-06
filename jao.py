#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, Job
from functools import wraps
import os
import time
import sys
import configparser
import logging
import xkcd
import notifyroles
import utility

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('jao.ini')

def start(bot, update):
    update.message.reply_text("I°_°I\nCommencing opperation...")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
    
def main():
    updater = Updater(config['KEY']['api_key'])
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    # setting up xkcd commands
    dp.add_handler(CommandHandler("xkcd", xkcd.get,
                                  pass_args=True))
    dp.add_handler(CommandHandler("join",
                                  notifyroles.join,
                                  pass_args=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("create_role",
                                  notifyroles.create_role,
                                  pass_args=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("notify",
                                  notifyroles.notify,
                                  pass_args=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("leave",
                                  notifyroles.leave,
                                  pass_args=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("roles",
                                  notifyroles.list_roles,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("restart",
                                  restart))
    dp.add_error_handler(error)
    
    #start bot activity
    updater.start_polling()
    updater.idle()

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if str(user_id) not in config['KEY']['higher_privileges']:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

@restricted
def restart(bot, update):
    bot.send_message(update.message.chat_id, "Bot is restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
    main()
