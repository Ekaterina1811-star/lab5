import requests
import matplotlib.pyplot as plt
from datetime import datetime


from jira_api import fetch_jira_issues  # Импорт функции для запросов к JIRA
# Получаем задачи из JIRA
issues = fetch_jira_issues("KAFKA")  # Подставляем нужный проект

if not issues:
    print('Нет данных по задачам')
else:
    print(f"Загружено {len(issues)} задач.")  # len(issues) возвращает количество элементов в списке


# Сбор данных о времени, проведенном в открытом состоянии
open_times = []
for issue in issues:
    created = datetime.strptime(issue['fields']['created'], "%Y-%m-%dT%H:%M:%S.%f%z")
    closed = datetime.strptime(issue['fields']['resolutiondate'], "%Y-%m-%dT%H:%M:%S.%f%z")
    open_time = (closed - created).days  # Количество дней в открытом состоянии
    open_times.append(open_time)

# Построение гистограммы
bin_size = 25
bins = range(0, max(open_times)+bin_size, bin_size)
plt.hist(open_times, bins=bins, alpha=0.8, color='skyblue', edgecolor='blue')
plt.xlabel('Время (дни)')
plt.ylabel('Количество задач')
plt.title('Время задач в открытом состоянии')
plt.xticks(range(0, max(open_times) + bin_size, 2*bin_size))
# Ограничиваем диапазон оси X до 365 дней (можно изменить на нужное значение)
plt.xlim(0,365)
plt.grid(axis='y')
plt.show()