"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход 
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите 
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите 
  бота отвечать, в каком созвездии сегодня находится планета.

"""
import logging
import datetime
import ephem

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

# Объявляем конфиг бота
logging.basicConfig(filename='bot.log', level=logging.INFO)

# Функция-обработчик команды /start
def greet_user(update, context):
	update.message.reply_text('Привет!')
	
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
	
# Функция-обработчик текстовых сообщений	
def talk_to_me(update, context):
	update.message.reply_text(update.message.text)

def main():
	# Объявляем бота с полученным токеном
	mybot = Updater(settings.API_KEY, use_context=True)

	# Объявление диспетчера и описание хендлеров
	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user))
	dp.add_handler(CommandHandler("planet", show_constellation))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))
	
	# Запускаем апдейтер и пишем это в лог
	logging.info("Bot started")
	mybot.start_polling()
	mybot.idle()
	
if __name__ == "__main__":	
	main()
