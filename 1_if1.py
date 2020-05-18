"""

Домашнее задание №1

Условный оператор: Возраст

* Попросить пользователя ввести возраст при помощи input и положить 
  результат в переменную
* Написать функцию, которая по возрасту определит, чем должен заниматься пользователь: 
  учиться в детском саду, школе, ВУЗе или работать
* Вызвать функцию, передав ей возраст пользователя и положить результат 
  работы функции в переменную
* Вывести содержимое переменной на экран

"""

def get_occupation(age):
	if age < 0:
		return 'Сначала родись, человек'
	elif 0 <= age < 7:
		return 'Учись в детском саду, человек'
	elif 7 <= age < 17:
		return 'Учись в школе, человек'
	elif 17 <= age < 21:
		return 'Учись в ВУЗе, человек'
	elif 21 <= age < 70:
		return 'Иди работай, человек'
	else:
		return 'Можешь наконец отдохнуть, человек'
	

def main():
	while True:
		age = input('Введите ваш возраст: ')
		try:
			age = int(age)
			break
		except:
			print('Введите числовое значение!')
	occupation = get_occupation(age)
	print (occupation)

if __name__ == "__main__":
    main()
