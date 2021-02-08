mHelpText = "это справка\n" \
            "/help -- этот текст\n" \
            "/start -- начать заного\n" \
            "/select_theme -- выбрать тему"
mNotUnderstandText = "такой комманды не существует! \n Спавка доступна по комманде /help"
def getHelpText():
    global mHelpText
    return mHelpText
def getNotUnderstandText():
    global mNotUnderstandText
    return mNotUnderstandText