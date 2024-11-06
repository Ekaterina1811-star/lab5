import matplotlib.pyplot as plt
from collections import defaultdict
from jira_api import analyse_time_spent

 # Запрос к JIRA для получения задач с полем timespent
issues = analyse_time_spent("KAFKA")
    # Проверяем, что данные получены
if not issues:
        print('Нет данных о закрытых задачах с затраченным временем')
else:
        print(f"Загружено {len(issues)} задач.")

def task5(issues):
    # Словарь для хранения количества задач по времени выполнения
    time_spent_counts = defaultdict(int)

    for issue in issues:
        time_spent = issue['fields'].get('timespent')
        if time_spent: # Проверка, если поле `timespent` не пустое
            time_spent_hours = time_spent / 3600 # Переводим секунды в часы
            time_spent_counts[time_spent_hours] += 1

    # Построение гистограммы
    times = list(time_spent_counts.keys()) # возвращает все ключи из словаря (разные значения времени)
    counts = list(time_spent_counts.values()) # возвращает все значения из time_spent_counts (количество задач для каждого значения времени)

    plt.figure(figsize=(10, 6))
    plt.bar(times, counts, color='skyblue')
    plt.xlabel('Затраченное время (часы)')
    plt.ylabel('Количество задач')
    plt.title('Гистограмма затраченного времени на выполнение задач')
    plt.grid(axis='y')
    plt.xticks(range(0, int(max(times))+1, 10)) # задает последовательность чисел от 0 до int(max(times)) + 1 с шагом 10
    plt.show()


task5(issues)



