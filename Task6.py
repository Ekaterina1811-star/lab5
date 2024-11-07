import matplotlib.pyplot as plt
from collections import defaultdict
from jira_api import analyse_issues_with_priority

# Запрос к JIRA для получения задач с полем priority
issues = analyse_issues_with_priority("KAFKA")

if not issues:
    print('Нет данных по задачам')
else:
    print(f"Загружено {len(issues)} задач.")  # len(issues) возвращает количество элементов в списке

def task6(issues):
    priority_counts = defaultdict(int)  # Словарь для подсчета количества задач по каждой степени серьезности (ключи - разные приоритеты задач, а значения — количество задач для каждого приоритета)
    # Подсчитываем количество задач для каждой степени приоритета
    for issue in issues:
        priority = issue['fields'].get('priority', {}).get('name')  # fields - словарь, priority - ключ, name - подключ
        #  .get('priority', {}) возвращает словарь с информацией о приоритете задачи (или пустой словарь {}, если приоритет отсутствует
        if priority:
            priority_counts[priority] += 1

    # Подготовка данных для графика
    priorities = list(priority_counts.keys())
    counts = list(priority_counts.values())

    print("Количество задач по каждому приоритету:")
    for priority, count in priority_counts.items():
        print(f"Приоритет'{priority} : {count} задач")

    # Построение гистограммы
    plt.figure(figsize=(10, 10))
    plt.bar(priorities, counts, color='skyblue', edgecolor='blue')
    plt.xlabel('Приоритет задачи')
    plt.ylabel('Количество задач')
    plt.title('Распределение задач по приоритету')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()



task6(issues)


