"""

Домашнее задание №1

Исключения: KeyboardInterrupt

* Перепишите функцию ask_user() из задания while2, чтобы она 
  перехватывала KeyboardInterrupt, писала пользователю "Пока!" 
  и завершала работу при помощи оператора break
    
"""

def ask_user():
	q_a = {
		"Как дела?": "Хорошо!", 
		"Что делаешь?": "Программирую",
		"Как погода?": "Норм",
		"Всё работаешь?": "Ага"
	}
	while True:
		try:
			user_input = input('Введите вопрос:\r\n')
			try:
				print(q_a[user_input], end = '\r\n\r\n')
			except:
				print('Вопрос не найден!\r\n')
		except KeyboardInterrupt:
			print('\r\nПока!')
			break
		
    
if __name__ == "__main__":
	ask_user()
