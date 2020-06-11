"""
 Научите бота играть в города. Правила такие - внутри бота есть список городов, пользователь пишет /cities Москва и если в списке такой город есть, бот отвечает городом на букву "а" - "Альметьевск, ваш ход". Оба города должны удаляться из списка.

    Помните, с ботом могут играть несколько пользователей одновременно

"""
"""
 Научите бота выполнять основные арифметические действия с двумя числами: сложение, вычитание, умножение и деление. Если боту дать команду /calc 2-3, он должен ответить “-1”.

    Не забудьте обработать возможные ошибки во вводе: пробелы, отсутствие чисел, деление на ноль
    Подумайте, как можно сделать поддержку действий с тремя и более числами
"""

import logging
import datetime
import ephem
import settings
import random 

from collections import defaultdict
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler



# Объявляем конфиг логирования бота
logging.basicConfig(filename='bot.log', level=logging.INFO)


# Функция перебирает переданное слово с конца и возвращает первую валидную (не ыъьй) букву
def validate_letters(word):
    for letter in word[::-1]:
        if letter not in 'ыъьй':
            return letter
        else:
            pass


# Функция-обработчик команды /start
def greet_user(update, context):
    update.message.reply_text('Привет!')
    
    
# Функция-обработчик команды /calc    
def calc(update, context):
    equation = update.message.text[6:].replace(' ','').replace(',','.')
    if equation == '':
        update.message.reply_text('Пожалуйста введите желаемое уравнение в формтате "/calc уравнение".')
    else:
        try:
            update.message.reply_text(eval(equation))
        except (NameError, SyntaxError, ZeroDivisionError): 
            update.message.reply_text('В введенном уравнении присутвуют недопустимые символы, попробуйте снова.')

    
# Функция-обработчик команды /cities
def cities_start(update, context):
    update.message.reply_text('Инициализация игры в города')
    # Открываем локальный файл с городами и забираем из него всё содержимое в переменную
    with open('cities.txt', 'r', encoding='utf-8') as file:
        file_content = file.read()
    
    # Создаем список со всеми городами из считанного файла, приводим все города к нижнему регистру, заменяем "ё" на "е" для простоты
    city_list = ([i.lower().replace('ё','е') for i in file_content.split()])
    # Создаем словарь со списком городов, где ключи - первые буквы городов
    words_dict = defaultdict(list)
    # Загружаем ключи в словарь
    words_dict = {city[0]:[] for city in city_list}
    # Присваиваем ключам в словаре списки городов
    for city in city_list:
        words_dict[city[0]].append(city)
    context.user_data['dicts'] = words_dict
    context.user_data['last_letter'] = None

    update.message.reply_text('Инициализация завершена - напишите город чтобы начать. Чтобы выйти из игры напишите "Стоп"')
    
    return cities_in_progress
    
    
def cities_in_progress(update, context):
    if update.message.text.lower() == "стоп":
        update.message.reply_text("Спасибо за игру, если захотите сыграть еще раз - просто напишите /cities")
        return ConversationHandler.END
    # Проверяем, что присланный город начинается с последней буквы города, который отправил бот, проверка на None нужна для первого запуска, когда бот еще не вывел ниодного города
    if context.user_data['last_letter'] == None or context.user_data['last_letter'] == update.message.text.lower()[0]:
        # Пытаемся удалить из словаря город, который прислал пользователь, если не удается - зацикливаем запрос города
        try:
            context.user_data['dicts'].get(update.message.text.lower()[0]).remove(update.message.text.lower())
        except (ValueError, AttributeError):
            if context.user_data['last_letter'] == None:
                reply_end = '.'
            else:
                reply_end = f", название города должно начинаться с буквы {context.user_data['last_letter'].capitalize()}"
            update.message.reply_text(f"Такого города я не знаю, либо он уже был назван :( Попробуйте еще раз{reply_end}")
            return cities_in_progress
        # Выгружаем из словаря все подходящие города списком
        candidate_words_list = context.user_data['dicts'].get(validate_letters(update.message.text))
        # Если слова в словаре на последнюю букву присланного города закончились - бот проигрывает
        if len(candidate_words_list) == 0:
            update.message.reply_text("Поздравляю, вы победили! Если захотите сыграть еще раз - просто напишите /cities")
            return ConversationHandler.END
        else:
            # Рандомно выбираем город из выгруженного списка
            word = candidate_words_list[random.randint(0,len(candidate_words_list)-1)]
            # Удаляем выбранный город из словаря
            context.user_data['dicts'].get(word[0]).remove(word)
            # Сохраняем последнюю букву из выбранного слова для последующей проверки
            context.user_data['last_letter'] = validate_letters(word)
            # Отдаем выбранный город пользователю и зацикливаем функцию
            update.message.reply_text(word.capitalize())
            # Если в словаре больше нет слов, начинающихся с последней буквы выбранного слова - юзер проигрывает
            if len(context.user_data['dicts'].get(context.user_data['last_letter'])) == 0:
                update.message.reply_text("Я победил :Р Если хотите попытаться еще раз - просто напишите /cities")
                return ConversationHandler.END
    else:
        update.message.reply_text(f"Первая буква города не совпадает с последней в отправленном мною городе :( Попробуйте еще раз, название города должно начинаться с буквы {context.user_data['last_letter'].capitalize()}")
    return cities_in_progress
 

# Фейковая функция, не знаю как сделать без её создания
def cancel(update, context):
    return ConversationHandler.END

    
# Функция-обработчик команды /planet
def show_constellation(update, context):
    current_date = f"{datetime.datetime.now():%Y/%m/%d}"
    command, planet = update.message.text.split()
    try:
        # Делаем какую-то переменную с вводом пользователя и сегодняшней датой (не знаю как это работает, но работает)
        planet_today = getattr(ephem, planet)(current_date)
        # Получаем список созвездий, конвертим его из tuple в list
        constellation1, constellation2 = list(ephem.constellation(planet_today))
        # К сожалению ничего не знаю может ли планета быть в 3-х созвездиях, но допустим что не может
        update.message.reply_text(f'Сегодня данная планета находится в созвездиях {constellation1} и {constellation2}.')
    except AttributeError:
        update.message.reply_text('Имя планеты не найдено, попробуйте снова.')

        
# Функция-обработчик команды /wordcount
def wordcount(update, context):
    # Конвертим сообщение пользовтеля в список
    user_input = update.message.text.split()
    # Получаем длину вообщения пользователя за исключением самой команды, т.е. -1
    input_lenght = len(user_input) - 1
    update.message.reply_text(f'Количество слов в вашем сообщении - {input_lenght}')

    
# Функция-обработчик текстовых сообщений    
def talk_to_me(update, context):
    update.message.reply_text(update.message.text)


# Функция-обработчик команды /next_full_moon
def next_full_moon(update, context):
    # Записываем сегодняшнюю дату в список
    current_date = f"{datetime.datetime.now():%Y/%m/%d}"
    # Получаем дату ближайшего полнолуния в формате ephem.date, конвертим его в строку и разбиваем на две переменные - дату и время
    next_moon_date, next_moon_time = str(ephem.next_full_moon(current_date)).split()
    update.message.reply_text(f'Следующее полнолуние произойдет {next_moon_date} в {next_moon_time}')


def main():
    # Объявляем бота с полученным токеном
    mybot = Updater(settings.API_KEY, use_context=True)

    # Объявление диспетчера и описание хендлеров
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", show_constellation))
    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler("calc", calc))
    #dp.add_handler(CommandHandler("cities", cities))
    dp.add_handler(ConversationHandler(
        entry_points = [CommandHandler("cities", cities_start)],
        states = {cities_in_progress:[MessageHandler(Filters.text, cities_in_progress)]},
        fallbacks = [CommandHandler("cancel", cancel)]
    ))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    # Запускаем апдейтер и пишем это в лог
    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()
    
    
if __name__ == "__main__":    
    main()