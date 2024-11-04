import requests # Импортируем библиотеку для выполнения HTTP-запросов
def fetch_jira_issues(project_key):
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
