"""

Домашнее задание №1

Цикл for: Оценки

* Создать список из словарей с оценками учеников разных классов 
  школы вида [{'school_class': '4a', 'scores': [3,4,4,5,2]}, ...]
* Посчитать и вывести средний балл по всей школе.
* Посчитать и вывести средний балл по каждому классу.
"""

def school_average(classes):
	students_quantity, students_scores = 0, 0
	for elem in classes:
		students_quantity += len(elem['scores'])
		students_scores += sum(elem['scores'])
	print (f'Средний балл по всей школе составляет {round(students_scores/students_quantity,2)}\r\n')

def class_average(classes):
	for elem in classes:
		print(f"Средний бал по классу {elem['school_class']} составляет {round(sum(elem['scores'])/len(elem['scores']),2)}")

def main():
	classes = [
		{'school_class': '4a', 'scores': [3,4,4,5,2]},
		{'school_class': '4b', 'scores': [2,4,5,3,4,5,4]},
		{'school_class': '4c', 'scores': [5,5,4,5,5]},
		{'school_class': '4d', 'scores': [2,2,3,4,2,2]},
		{'school_class': '4e', 'scores': [5,3,5,3,5,3,5,3,5,3,5,2,2,2]},
	]
	school_average(classes)
	class_average(classes)
    
if __name__ == "__main__":
    main()
