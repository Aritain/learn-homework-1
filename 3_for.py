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
	all_scores = [score for item in classes for score in item['scores']]
	average_score = round(sum(all_scores)/len(all_scores),2)
	print (f'Средний балл по всей школе составляет {average_score}\r\n')

def class_average(classes):
	for elem in classes:
		average_class_score = round(sum(elem['scores'])/len(elem['scores']),2)
		print(f"Средний бал по классу {elem['school_class']} составляет {average_class_score}")

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
