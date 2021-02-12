import telebot
from telebot import types
import StringsAdapter as strings
import datetime
import Kinematics
import time


import Kinematics

f = open("logs/errors_reports/n.txt", "r")
n = int(f.read())
f.close()
print(n)

bot = telebot.TeleBot('1627441769:AAHBpKzT0XPuLPT2fvOGOn2EPSlogs8xXp8')



@bot.message_handler(commands=['start'])
def startText(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('Выбрать тему')
    btn2 = types.KeyboardButton('Справка')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Привет!\nЭто физический бот-калькулятор \nнапиши /help чтобы получить справку", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    m = message.text.lower()
    # Help
    if m == '/help' or m == "справка":
        bot.send_message(message.from_user.id, strings.HelpText, reply_markup=types.ReplyKeyboardRemove())

    # Authors
    elif m == "/authors":
        bot.send_message(message.from_user.id, "Авторы: \nDanila Yarmarkin ПФМЛ №239 г. Санкт-Петербурга", reply_markup=types.ReplyKeyboardRemove())

    # Error report
    elif m == "/error_report":
        bot.send_message(message.from_user.id, 'опишите проблему', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, makeReport)

    # Select theme
    elif m in strings.selectTextCommands:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Кинематика')
        btn2 = types.KeyboardButton('Динамика')
        btn3 = types.KeyboardButton('Электростатика')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         "Выберите тему",
                         reply_markup=markup)
    # Kinematics
    elif m in strings.kinematicsCommands:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Баллистика')
        btn2 = types.KeyboardButton('Прямолинейное движение')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(message.chat.id,
                         "Выберите тему в теме \"Кинематика\"",
                         reply_markup=markup)
    # Ballistics
    elif m in strings.ballisticsCommands:
        bot.send_message(message.chat.id, "Тема Баллистика", reply_markup=types.ReplyKeyboardRemove())
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Калькулятор считает время полета, дальность полета, конечную скорость тела, "
                                          "максимальную высоту полета тела и угол падения тела из начальной высоты тела,"
                                          " начальной скорости тела и угла между вектором начальной скорости тела и горизонтом")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('/start_ballistics')
        markup.add(btn1)
        bot.send_message(message.chat.id, "Бот считает данные без сопротивления воздуха", reply_markup=markup)
        bot.send_message(message.chat.id, "напишите /start_ballistics чтобы начать")

    # Ballistic start
    elif m == "/start_ballistics":
        bot.send_message(message.chat.id, "Введите начальную высоту тела (м)", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, getStartHeigh)

    else:
        bot.send_message(message.from_user.id, strings.NotUnderstandText, reply_markup=types.ReplyKeyboardRemove())

def makeReport(message):
    global n
    try:
        now = datetime.datetime.now()
        author = message.from_user.first_name + " " + message.from_user.last_name
        print("error report:", message.text)
        f = open("logs/errors_reports/log"+str(n)+".log", "w")
        n += 1
        f.write("Автор: " + author)
        f.write("\n")
        f.write("Дата и время: ")
        f.write(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + ":" + str(now.microsecond) + "  " + str(now.day) + "." + str(now.month) + "." + str(now.year))
        f.write("\n")
        f.write("Текст отчета: ")
        f.write(message.text)
        f.close()
        f = open("logs/errors_reports/n.txt", "w")
        f.write(str(n))
        f.close()
        bot.send_message(message.from_user.id, strings.ThanksForErrorReportMessage)
    except Exception:
        print("e")


# Ballistic
g = 10
alpha = 0
startSpeed = 0
startHeight = 0

def ballisticError():
    global g, alpha, startHeight, startSpeed
    g = 0
    alpha = 0
    startSpeed = 0
    startHeight = 0

def getStartHeigh(message):
    global startHeight
    try:
        startHeight = float(message.text)
        bot.send_message(message.chat.id, "Введите начальную скорость тела (м/c)")
        bot.register_next_step_handler(message, getStartSpeed)
    except TypeError:
        bot.send_message(message.from_user.id, "неверный формат данных")
        bot.register_next_step_handler(message, get_text_messages)
        ballisticError()
    except ValueError:
        bot.send_message(message.from_user.id, "неверный формат данных")
        bot.register_next_step_handler(message, get_text_messages)
        ballisticError()

def getStartSpeed(message):
    global startSpeed
    try:
        startSpeed = float(message.text)
        bot.send_message(message.chat.id, "Введите угол (градусы)")
        bot.register_next_step_handler(message, getAlpha)
    except TypeError:
        bot.send_message(message.from_user.id, "неверный формат данных")
        bot.register_next_step_handler(message, get_text_messages)
        ballisticError()
    except ValueError:
        bot.send_message(message.from_user.id, "неверный формат данных")
        bot.register_next_step_handler(message, get_text_messages)
        ballisticError()

def getAlpha(message):
    global alpha
    try:
        alpha = float(message.text)
        bot.send_message(message.chat.id, "Введите ускрение свободного падения g (м/с^2)")
        bot.register_next_step_handler(message, getG)
    except TypeError:
        bot.send_message(message.from_user.id, "неверный формат данных")
        bot.register_next_step_handler(message, get_text_messages)
        ballisticError()
    except ValueError:
        bot.send_message(message.from_user.id, "неверный формат данных")
        bot.register_next_step_handler(message, get_text_messages)
        ballisticError()

def getG(message):
    global g, startSpeed, startHeight, alpha
    try:
        g = float(message.text)
        bot.send_message(message.chat.id, "Производятся рассчеты...")
        b = Kinematics.Ballistics(startSpeed, startHeight, alpha, g)
        bot.send_message(message.chat.id, "Время полета " + str(b.time) + " с")
        bot.send_message(message.chat.id, "Дальность полета " + str(b.len) + " м")
        bot.send_message(message.chat.id, "Конечная скорость " + str(b.endSpeed) + " м/с")
        bot.send_message(message.chat.id, "Максимальная высота полета " + str(b.maxHeight) + " м")
        bot.send_message(message.chat.id, "Угол падения " + str(b.phi) + u" \u00b0")
        ballisticError()
    except TypeError:
        bot.send_message(message.from_user.id, "неверный формат данных")
        bot.register_next_step_handler(message, get_text_messages)
        ballisticError()
    except ValueError:
        bot.send_message(message.from_user.id, "неверный формат данных")
        bot.register_next_step_handler(message, get_text_messages)
        ballisticError()

bot.polling(none_stop=True)
if __name__ == '__main__':
    bot.infinity_polling()