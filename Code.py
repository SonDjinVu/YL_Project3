import random
import sqlite3
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
named_cities = []


def answer(update, context):
    ok_cities = []
    string = update.message.text
    string = string.capitalize()
    con = sqlite3.connect('Cities.db')
    cur = con.cursor()
    text = cur.execute("SELECT id FROM Cities WHERE name=?;", (string,)).fetchone()
    if type(text) != tuple:
        text = (0,)
    if text[0] != 0:
        cities = cur.execute("SELECT name FROM Cities;").fetchall()
        previous_message = named_cities[-1]
        city = cur.execute("SELECT name FROM Cities WHERE id=?;", (previous_message, )).fetchone()
        string = string.lower()
        if city[0][-1] == string[0] and city[0][-1] != 'ь':
            flag = 1
        elif city[0][-2] == string[0]:
            flag = 1
        else:
            flag = 0
        if flag == 1:
            if text[0] in named_cities:
                update.message.reply_text('Этот город уже был назван. Пожалуйста, введите другой.')
            else:
                named_cities.append(text[0])
                x = 1
                string = string.upper()
                while True:
                    for i in range(len(cities)):
                        print(cities[i][0])
                        city3 = cur.execute("SELECT id FROM Cities WHERE name=?;", (cities[i][0],)).fetchone()
                        print(city3)
                        print(named_cities)
                        if cities[i][0][0] == string[-x] and string[-1] != "Ь" and city3[0] not in named_cities:
                            ok_cities.append(cities[i][0])
                        elif cities[i][0][0] == string[-(x + 1)] and city3[0] in named_cities:
                            ok_cities.append(cities[i][0])
                    if len(ok_cities) != 0:
                        break
                    else:
                        x += 1
                city2 = ok_cities[random.randint(0, len(ok_cities) - 1)]
                update.message.reply_text(city2)
                text = cur.execute("SELECT id FROM Cities WHERE name=?;", (city2,)).fetchone()
                named_cities.append(text[0])
        else:
            update.message.reply_text('''Вы назвали город, который начинается не на нужную букву. Пожалуйста, введите ещё раз.''')
    else:
        update.message.reply_text('Похоже, что вы назвали несуществующий в России город. Попробуйте ещё раз')


def start(update, context):
    named_cities[:] = []
    con = sqlite3.connect('Cities.db')
    cur = con.cursor()
    text = cur.execute("SELECT name FROM Cities WHERE id=?;", (random.randint(1, 3),)).fetchone()
    update.message.reply_text("Давайте сыграем в города! Я начну с города " + text[0])
    city = cur.execute("SELECT id FROM Cities WHERE name=?;", (text[0],)).fetchone()
    named_cities.append(city[0])


def main():
    updater = Updater("1702641048:AAFH2jlOS4ATGXvX7YIJxnNN1SShpXYeBzc", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()