# -*- coding: utf-8 -*-
import configparser
from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler
from bot import BotAPI

config = configparser.ConfigParser()
config.read('config.cfg')


def tele_bot(bot, m):
    answ_data = BotAPI(m.message.text)
    chat_id = m.message.chat_id
    answ = [answ_data.answ[i:i + 4000] for i in range(0, len(answ_data.answ), 4000)]
    for a in answ:
        bot.sendMessage(chat_id=chat_id, text=a,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=ReplyKeyboardMarkup(answ_data.keypad))


if __name__ == "__main__":
    updater = Updater(config.get('Telegram', 'token'),
                      request_kwargs={'proxy_url': config.get('Proxy', 'address'),
                                      'urllib3_proxy_kwargs': {'username': config.get('Proxy', 'username'),
                                                               'password': config.get('Proxy', 'password')}})
    updater.dispatcher.add_handler(MessageHandler(Filters.all, tele_bot))
    updater.start_polling()
    updater.idle()
