import datetime # Импортируем модуль datetime для работы с датами и временем
import matplotlib.pyplot as plt # Импортируем pyplot из библиотеки matplotlib, чтобы строить графики.
from collections import defaultdict # Импортируем defaultdict из модуля collections, чтобы удобно работать со словарями, автоматически задавая значения по умолчанию для отсутствующих ключей.
import requests # Импортируем библиотеку для выполнения HTTP-запросов


from jira_api import get_project_issues  # Импорт функции для запросов к JIRA
# Получаем задачи из JIRA
issues = get_project_issues("KAFKA")  # Подставляем нужный проект

# Проверяем, что `issues` не пустой
if not issues:
    print("Данные о задачах не загружены.")
else:
    print(f"Загружено {len(issues)} задач.")

    def task3(issues):
        """
            Анализирует задачи и строит график, показывающий количество созданных и закрытых задач в день,
            а также накопительный итог по задачам.
            """
        created_task_counts = defaultdict(int) # словарь хранит количество созданных задач по датам
        closed_task_counts = defaultdict(int) # словарь для хранения количества закрытых задач по датам

        # Заполнение словарей с датами создания и закрытия задач
        for issue in issues:
            created_date = datetime.datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z').date() # Преобразуем строку даты создания задачи issue['fields']['created'] в объект datetime
            created_task_counts[created_date] += 1
            # Проверяем, если задача закрыта, преобразуем дату закрытия и увеличиваем счетчик задач на эту дату
            if issue['fields']['resolutiondate']:
                closed_date = datetime.datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
                closed_task_counts[closed_date] += 1

        # Вычисление минимальной и максимальной дат для установления диапазона графика
        min_date = min(created_task_counts.keys() | closed_task_counts.keys()) # Находим min дату из объединенных ключей двух словарей
        max_date = max(created_task_counts.keys() | closed_task_counts.keys()) # Находим max дату из всех дат создания и закрытия задач

        # Генерация списка всех дат в указанном диапазоне
        all_dates = [min_date + datetime.timedelta(days=x) for x in range((max_date - min_date).days + 1)] # список all_dates содержит все даты от min_date до max_date, с шагом в один день
        # Инициализация переменных для накопительного подсчета задач
        daily_created_counts = [] #  Список для хранения количества созданных задач для каждой даты
        daily_closed_counts = [] #  Список для хранения количества закрытых задач для каждой даты
        cumulative_opened_total = 0 # Переменная для накопительного счета созданных задач.
        cumulative_closed_total = 0 #  Переменная для накопительного счета закрытых задач
        cumulative_created_series = [] #  Список для накопительных итогов по созданным задачам
        cumulative_closed_series = [] # Список для накопительных итогов по закрытым задачам

        # Заполнение списков для данных на график
        for date in all_dates:
            daily_created_counts.append(created_task_counts.get(date, 0)) # Получаем ежедневное количество созданных и закрытых задач
            daily_closed_counts.append(closed_task_counts.get(date, 0))  # Добавляем в daily_closed_counts количество задач, закрытых на текущую дату date. Если задач на эту дату нет, подставляется 0
            # как менялось количество созданных и закрытых задач по дням

            # Подсчет накопительного итога
            cumulative_opened_total += daily_created_counts[-1]
            cumulative_closed_total += daily_closed_counts[-1]

            # Добавляем данные о накопительном итоге в соответствующие списки
            cumulative_created_series.append(cumulative_opened_total)
            cumulative_closed_series.append(cumulative_closed_total)

            # Построение графика
        plt.figure(figsize=(12, 6))



        # Линии для ежедневного количества заведенных и закрытых задач
        plt.plot(all_dates, daily_created_counts, label = 'Ежедневное количество заведенных задач', color = 'blue')
        plt.plot(all_dates, daily_closed_counts, label = 'Ежедневное количество закрытых задач', color = 'green')

        # Линии накопительного итога для заведенных и закрытых задач
        plt.plot(all_dates, cumulative_created_series, label='Накопленный итог заведенных задач', color='blue', linestyle='--')
        plt.plot(all_dates, cumulative_closed_series, label='Накопленный итог закрытых задач', color='red', linestyle='-.')

        # Настройка осей и отображение легенды
        plt.xlabel('Дата')
        plt.ylabel('Количество задач')
        plt.title('График создания и закрытия задач с накопительным итогом')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

task3(issues)










