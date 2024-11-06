import requests # Импортируем библиотеку для выполнения HTTP-запросов
def fetch_jira_issues(project_key): # для первой и второй задачи
    """Запрашивает задачи из JIRA для указанного проекта."""
    url = "https://issues.apache.org/jira/rest/api/2/search" #URL для JIRA API
    params = {
        "jql": f"project={project_key} AND status=Closed", # Строка запроса: задачи в проекте `project_key`, статус — `Closed`
        "fields": "created, resolutiondate, status, statuscategorychangedate", # Поля, которые запрашиваем: дата создания и закрытия
        "expand": "changelog", # API JIRA возвращает полный набор изменений для каждой задачи
        "maxResults": 1000 # Максимальное количество задач, которые хотим получить

    }
    response = requests.get(url, params=params) # Выполняем GET-запрос к JIRA API с параметрами
    response.raise_for_status() # Проверяем успешность запроса (вызывает ошибку при неудаче)
    data = response.json() # Преобразуем ответ из JSON в словарь Python
    return data.get("issues", []) # Извлекаем список задач из данных или пустой список, если задач нет


def get_project_issues(project_key): # для 3 задачи
    """Запрашивает задачи из JIRA для указанного проекта."""
    url = "https://issues.apache.org/jira/rest/api/2/search" #URL для JIRA API
    params = {
        "jql": f"project={project_key} AND status in (Open, Closed) AND created >= -60d ", # Строка запроса: задачи в проекте `project_key`, статус — `Closed`
        "fields": "created, resolutiondate, status, statuscategorychangedate", # Поля, которые запрашиваем: дата создания и закрытия
        "expand": "changelog", # API JIRA возвращает полный набор изменений для каждой задачи
        "maxResults": 1000 # Максимальное количество задач, которые хотим получить

    }
    response = requests.get(url, params=params) # Выполняем GET-запрос к JIRA API с параметрами
    response.raise_for_status() # Проверяем успешность запроса (вызывает ошибку при неудаче)
    data = response.json() # Преобразуем ответ из JSON в словарь Python
    return data.get("issues", []) # Извлекаем список задач из данных или пустой список, если задач нет

def get_assignee_issues(project_key): # для 4 задачи
    url = "https://issues.apache.org/jira/rest/api/2/search"  # URL для JIRA API
    params = {
        "jql": f"project={project_key} AND assignee IS NOT EMPTY AND reporter IS NOT EMPTY ",
        # Строка запроса: задачи в проекте `project_key`, статус — `Closed`
        "fields": "assignee, reporter",
        # Поля, которые запрашиваем: дата создания и закрытия
        "expand": "changelog",  # API JIRA возвращает полный набор изменений для каждой задачи
        "maxResults": 1000  # Максимальное количество задач, которые хотим получить

    }
    response = requests.get(url, params=params)  # Выполняем GET-запрос к JIRA API с параметрами
    response.raise_for_status()  # Проверяем успешность запроса (вызывает ошибку при неудаче)
    data = response.json()  # Преобразуем ответ из JSON в словарь Python
    return data.get("issues", [])


def analyse_time_spent(project_key): # для 5 задачи
    url = "https://issues.apache.org/jira/rest/api/2/search"  # URL для JIRA API
    params = {
        "jql": f'project="{project_key}" AND status=Closed',
        # Строка запроса: задачи в проекте `project_key`, статус — `Closed`
        "fields": "timespent",
        # Поля, которые запрашиваем: дата создания и закрытия
        "expand": "changelog",  # API JIRA возвращает полный набор изменений для каждой задачи
        "maxResults": 1000  # Максимальное количество задач, которые хотим получить

    }
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, params=params, headers=headers)  # Выполняем GET-запрос к JIRA API с параметрами
    response.raise_for_status()  # Проверяем успешность запроса (вызывает ошибку при неудаче)
    data = response.json()  # Преобразуем ответ из JSON в словарь Python

    # Отображение значений `timespent` для отладки
    for issue in data.get("issues", []):
        print("ID задачи:", issue.get("id"))
        print("Затраченное время (timespent):", issue['fields'].get('timespent'))

    return data.get("issues", [])

analyse_time_spent('Hadoop HDFS')



