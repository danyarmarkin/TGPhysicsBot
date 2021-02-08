import telebot
from telebot import types
import StringsAdapter as strings

bot = telebot.TeleBot('1627441769:AAHBpKzT0XPuLPT2fvOGOn2EPSlogs8xXp8')

selectTextCommands = ["выбрать тему", "тема", "/select_theme"]

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
    if m == '/help' or m == "справка":
        bot.send_message(message.from_user.id, strings.getHelpText(), reply_markup=types.ReplyKeyboardRemove())

    elif m in selectTextCommands:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Кинематика')
        btn2 = types.KeyboardButton('Динамика')
        btn3 = types.KeyboardButton('Электростатика')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         "Выберите тему",
                         reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, strings.getNotUnderstandText(), reply_markup=types.ReplyKeyboardRemove())


bot.polling(none_stop=True)
if __name__ == '__main__':
    bot.infinity_polling()