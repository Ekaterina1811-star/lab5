
import matplotlib.pyplot as plt # Импортируем pyplot из библиотеки matplotlib, чтобы строить графики.
from collections import defaultdict # Импортируем defaultdict из модуля collections, чтобы удобно работать со словарями, автоматически задавая значения по умолчанию для отсутствующих ключей.
import numpy as np


from jira_api import get_assignee_issues  # Импорт функции для запросов к JIRA
# Получаем задачи из JIRA
issues = get_assignee_issues("KAFKA")  # Подставляем нужный проект

# Проверяем, что `issues` не пустой
if not issues:
    print("Данные о задачах не загружены.")
else:
    print(f"Загружено {len(issues)} задач.")

def task_4(issues):
        user_task_counts = defaultdict(int) # Словарь для хранения количества задач для пользователей

        for issue in issues:
            assignee = issue['fields'].get('assignee', {}).get('displayName') # Получаем имя исполнителя
            reporter = issue['fields'].get('reporter', {}).get('displayName')
            # Увеличиваем счетчик для исполнителя, если он существуе
            if assignee:
                user_task_counts[assignee] += 1

            # Увеличиваем счетчик для репортера, если он существует
            if reporter:
                user_task_counts[reporter] += 1

        # Сортируем пользователей по количеству задач
        top_users = sorted(user_task_counts.items(), key=lambda x: x[1], reverse=True)[:30] # top_users будет содержать список кортежей вида [(пользователь, количество задач), ...] для 30 пользователей с наибольшим числом задач
        # Подготовка данных для графика
        usernames = [user[0] for user in top_users] # Извлекаем имена пользователей и количество задач
        task_counts = [user[1] for user in top_users]



        plt.figure(figsize=(15, 8))
        plt.barh(usernames, task_counts, color='skyblue')  # Горизонтальная гистограмма
        plt.xlabel('Количество задач')
        plt.ylabel('Пользователи')
        plt.title('Топ-30 пользователей по количеству задач')
        # Устанавливаем сетку и количество делений по оси X
        max_tasks = max(task_counts)  # Определяем максимальное количество задач
        x_ticks = np.arange(0, max_tasks + 1, 25)  # Интервал делений

        plt.xticks(x_ticks)  # Устанавливаем деления по X
        plt.grid(True, axis='x', linestyle='--', alpha=0.7)
        plt.gca().invert_yaxis()  # Инвертируем ось Y для отображения пользователя с максимальным количеством задач вверху
        plt.show()


task_4(issues)

