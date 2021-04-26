import random
import sqlite3
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
cities = []


def echo(update, context):
    string = update.message.text
    string = string.capitalize()
    con = sqlite3.connect('Cities.db')
    cur = con.cursor()
    text = cur.execute("SELECT id FROM Cities WHERE name=?;", (string,)).fetchone()
    if type(text) != tuple:
        text = (0,)
    if text[0] != 0:
        if text[0] in cities:
            update.message.reply_text('Этот город уже был назван. Пожалуйста, введите другой.')
        else:
            update.message.reply_text('Ема ты додик')
            cities.append(text[0])
    else:
        update.message.reply_text('Похоже, что вы назвали несуществующий в России город. Попробуйте ещё раз')
    print(cities)


def start(update, context):
    cities[:] = []
    con = sqlite3.connect('Cities.db')
    cur = con.cursor()
    text = cur.execute("SELECT name FROM Cities WHERE id=?;", (random.randint(1, 3),)).fetchone()
    update.message.reply_text("Давайте сыграем в города! Я начну с города " + text[0])
    city = cur.execute("SELECT id FROM Cities WHERE name=?;", (text[0],)).fetchone()
    cities.append(city[0])


def main():
    updater = Updater("1702641048:AAFH2jlOS4ATGXvX7YIJxnNN1SShpXYeBzc", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()