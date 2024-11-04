from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import requests


from jira_api import fetch_jira_issues  # Импорт функции для запросов к JIRA
# Получаем задачи из JIRA
issues = fetch_jira_issues("KAFKA")  # Подставляем нужный проект

# Проверяем, что `issues` не пустой
if not issues:
    print("Данные о задачах не загружены.")
else:
    print(f"Загружено {len(issues)} задач.")


# Функция для получения времени, проведенного в каждом статусе задачи
def get_status_times(issue):
    changelog = issue['changelog']['histories']  # Получаем историю изменений задачи
    status_times = {}  # Словарь для хранения времени по каждому статусу

    previous_status = 'Open'  # Начальный статус задачи
    previous_time = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')  # Начальный статус задачи, преобразование строки created (время создания задачи) в объект datetim

    for history in changelog: # цикл по всем элементам changelog, каждый элемент представляет одно изменение в истории задачи
        if 'field' in history['items'][0] and history['items'][0]['field'] == 'status':
            current_status = history['items'][0]['toString']

            # Выводим текущий статус
            print(f"Текущий статус: {current_status}") # выводит текущий статус для отслеживания

            current_time = datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')  # Время изменения статуса, преобразует время изменения статуса из строки в datetime
            time_spent = (current_time - previous_time).days  # Время, проведенное в предыдущем статусе

            # Игнорируем отрицательные значения времени
            if time_spent < 0:
                print(f"Пропускаем отрицательное значение времени для {previous_status} -> {current_status}")
                continue

            # Добавляем время к предыдущему статусу
            if previous_status in status_times: #проверяет, есть ли уже статус в status_times
                status_times[previous_status] += time_spent
            else:
                status_times[previous_status] = time_spent

            previous_status = current_status
            previous_time = current_time

    # Время в последнем статусе
    resolved_time = datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z')
    time_spent = (resolved_time - previous_time).days # сколько дней задача провела в последнем статусе

    if time_spent >= 0:  # Добавляем условие для отрицательного времени
        if previous_status in status_times:
            status_times[previous_status] += time_spent
        else:
            status_times[previous_status] = time_spent

    print(f"Статусы для задачи {issue['key']}: {status_times}")
    return status_times

    # Отладочная информация о времени для каждого статуса
    print(f"Задача: {issue['key']}, Время по статусам: {status_times}")

    return status_times


# Функция для построения гистограмм для каждого статуса
def task_2(issues):
    status_data = {}  # Словарь для хранения времени для каждого статуса

    # Заполняем словарь статусами и временем, проведенным в каждом из них
    for issue in issues:
        status_times = get_status_times(issue) # возвращает время, проведенное задачей в каждом статусе
        for status, time_spent in status_times.items():  # метод .items() используется, чтобы получить пары ключ-значение из словаря status_times в виде кортежей. Это позволяет вам обойти словарь и получить одновременно и ключ (статус задачи), и значение (время, проведенное в этом статусе).
            if status in status_data:
                status_data[status].append(time_spent)
            else:
                status_data[status] = [time_spent]

    # Проверяем и выводим информацию о статусах
    print("Собранные данные по статусам:")
    for status, times in status_data.items():
        print(f"Статус: {status}, Значения времени: {times}")

    # Строим диаграммы для каждого состояния
    for status, times in status_data.items():
        print(f"Построение графика для статуса '{status}' с {len(times)} значениями.")

        if len(times) == 0:
            print(f"Нет данных для статуса '{status}'. Пропускаем.")
            continue  # Пропустить, если нет данных

        # Строим полную гистограмму
        plt.hist(times, bins=40, edgecolor='blue', color='skyblue')
        plt.xlabel('Количество дней')
        plt.ylabel('Количество задач')
        plt.title(f'Время в статусе {status}')
        plt.grid(axis='y')
        plt.show()

        # Фильтруем данные для гистограммы с ограничением до 60 дней
        times_filtered = [t for t in times if t <= 60]
        if len(times_filtered) == 0:
            print(f"Нет данных для статуса '{status}' на меньшем интервале (<= 60 дней). Пропускаем.")
            continue  # Пропустить, если нет данных

        # Строим гистограмму с ограничением по времени
        plt.hist(times_filtered, bins=np.linspace(start=0, stop=60, num=41), edgecolor='blue', color='skyblue')
        plt.xlabel('Количество дней')
        plt.ylabel('Количество задач')
        plt.grid(axis='y')
        plt.title(f'Время в статусе {status} на меньшем интервале')
        plt.show()




task_2(issues)
