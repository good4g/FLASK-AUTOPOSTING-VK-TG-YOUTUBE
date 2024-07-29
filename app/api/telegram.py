import telebot


def post_tg(app, post):
    bot = telebot.TeleBot(app.config['TOKEN_TG_BOT'])
    id_chat = app.config['ID_CHAT_TG']
    bot.send_message(id_chat, post)