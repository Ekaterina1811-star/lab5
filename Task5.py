import matplotlib.pyplot as plt
from collections import defaultdict
from jira_api import analyse_time_spent

 # Запрос к JIRA для получения задач с полем timespent
issues = analyse_time_spent("ZOOKEEPER")
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
        if time_spent is not None: # Проверка, если поле `timespent` не пустое
            time_spent_hours = time_spent / 3600  # Переводим секунды в часы
            time_spent_counts[time_spent_hours] += 1
            print(f"ID задачи {issue['id']} ")
            print("Затраченное время", time_spent_hours)

        # else:
            # print(f"Задача с ID {issue['id']} не имеет залогированного времени.")

    # Построение гистограммы
    times = list(time_spent_counts.keys()) # возвращает все ключи из словаря (разные значения времени)
    counts = list(time_spent_counts.values()) # возвращает все значения из time_spent_counts (количество задач для каждого значения времени)

    plt.figure(figsize=(10, 6))
    #plt.bar(times, counts, color='skyblue', edgecolor='blue')
    counts, bins, patches = plt.hist(times, bins=25, color='skyblue', edgecolor='blue')
    plt.xlabel('Затраченное время (часы)')
    plt.ylabel('Количество задач')
    plt.title('Гистограмма затраченного времени на выполнение задач')
    plt.grid(axis='y')
    #plt.xticks(range(0, int(max(times))+1, 1)) # задает последовательность чисел от 0 до int(max(times)) + 1 с шагом 10

    # Печатаем количество задач в каждой корзине
    print("Количество задач в каждой корзине:")
    for i in range(len(counts)):
        print(f"Корзина {i + 1} (с интервалом от {bins[i]} до {bins[i + 1]}): {counts[i]} задач")

    plt.show()


task5(issues)



