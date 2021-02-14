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
    print(message.from_user.first_name, message.from_user.last_name, "(" + str(message.from_user.id) + "):", message.text)
    m = message.text.lower()
    # Help
    if m == '/help' or m == "справка":
        bot.send_message(message.from_user.id, strings.HelpText, reply_markup=types.ReplyKeyboardRemove())

    # Authors
    elif m == "/authors":
        bot.send_message(message.from_user.id, "Авторы: \nDanila Yarmarkin", reply_markup=types.ReplyKeyboardRemove())

    # Error report
    elif m == "/error_report":
        bot.send_message(message.from_user.id, 'Опишите проблему', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, makeReport)

    # Select theme
    elif m in strings.selectTextCommands:
        bot.send_message(message.chat.id, "Выберите тему\n"
                                          "Кинематика -- /kinematic\n"
                                          "Динамика -- /dynamic\n"
                                          "Экзамены 239 9 класс -- /239_exam_9", reply_markup=types.ReplyKeyboardRemove())
    #239 exams
    elif m == "/239_exam_9":
        bot.send_message(message.chat.id, "Выберите билет\n"
                                          "1 текст -- /239_exam_9_1\n"
                                          "1 pdf -- /239_exam_9_1_pdf\n"
                                          "2 -- /239_exam_9_2\n"
                                          "3 -- /239_exam_9_3\n"
                                          "4 -- /239_exam_9_4\n"
                                          "5 -- /239_exam_9_5\n"
                                          "6 -- /239_exam_9_6", reply_markup=types.ReplyKeyboardRemove())
    elif m == "/239_exam_9_1":
        bot.send_message(message.chat.id, 'Вы выбрали билет №1', reply_markup=types.ReplyKeyboardRemove())
        for i in strings.exam9Class.task1:
            bot.send_message(message.chat.id, i)
            time.sleep(0.1)
    elif m == "/239_exam_9_1_pdf":
        bot.send_document(message.chat.id, open('values/raw/exam_9_class/Bilet_1.pdf', 'rb'), reply_markup=types.ReplyKeyboardRemove())

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
        btn1 = types.KeyboardButton('/start_ballistic')
        btn2 = types.KeyboardButton('/formulas_ballistic')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "Бот считает данные без сопротивления воздуха", reply_markup=markup)
        bot.send_message(message.chat.id, "напишите /start_ballistic чтобы начать или /formulas_ballistic чтобы посмотреть формулы")

    # Ballistic start
    elif m == "/start_ballistic":
        bot.send_message(message.chat.id, "Введите начальную высоту тела (м)", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, getStartHeigh)

    # Ballistic formulas
    elif m == "/formulas_ballistic":
        bot.send_message(message.chat.id, "Вот формулы по баллистике", reply_markup=types.ReplyKeyboardRemove())
        bot.send_photo(message.chat.id, open('values/layouts/Kinematic/Ballistic/0.png', 'rb'))
        bot.send_photo(message.chat.id, open('values/layouts/Kinematic/Ballistic/1.png', 'rb'))
        bot.send_photo(message.chat.id, open('values/layouts/Kinematic/Ballistic/2.png', 'rb'))
        bot.send_photo(message.chat.id, open('values/layouts/Kinematic/Ballistic/3.png', 'rb'))
        bot.send_photo(message.chat.id, open('values/layouts/Kinematic/Ballistic/4.png', 'rb'))
        bot.send_photo(message.chat.id, open('values/layouts/Kinematic/Ballistic/5.png', 'rb'))
        bot.send_document(message.chat.id, open('values/layouts/Kinematic/Ballistic/formulas.pdf', 'rb'))

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

# =======Ballistic============
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
        bot.send_message(message.chat.id, "Если в ответе \"0\", то либо так и должно быть, "
                                          "либо введенные числа слишком большие")
        b = Kinematics.Ballistics(startSpeed, startHeight, alpha, g)
        bot.send_message(message.chat.id, "Время полета " + str(b.time) + " с")
        bot.send_message(message.chat.id, "Дальность полета " + str(b.len) + " м")
        bot.send_message(message.chat.id, "Конечная скорость " + str(b.endSpeed) + " м/с")
        bot.send_message(message.chat.id, "Максимальная высота полета " + str(b.maxHeight) + " м")
        bot.send_message(message.chat.id, "Угол падения " + str(b.phi) + u" \u00b0")
        ballisticError()
        del b
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
