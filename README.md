# Task Tracker API

Учебный проект таск-трекера на `Django REST Framework`.

## Что реализовано

- регистрация пользователей
- проекты с создателем и участниками
- задачи внутри проектов
- доступ к задачам только для участников проекта
- разграничение прав по ролям из ТЗ
- фильтрация задач
- пагинация
- Swagger и ReDoc

### Project

- `name` - название проекта
- `description` - описание проекта
- `creator` - создатель проекта
- `members` - участники проекта

### Task

- `project` - проект
- `title` - заголовок
- `description` - описание
- `priority` - приоритет
- `status` - статус
- `deadline` - дедлайн
- `author` - автор задачи
- `assignee` - исполнитель

## Права доступа

- участники проекта могут видеть только свои проекты и задачи
- владелец проекта может редактировать проект, управлять участниками и управлять любыми задачами проекта
- исполнитель задачи может менять `status` и `priority`
- автор задачи может менять `description` и удалять свою задачу

## Фильтрация задач

Доступны фильтры:

- `project`
- `status`
- `priority`
- `assignee`
- `deadline`
- `deadline_after`
- `deadline_before`

## Пагинация

Используется постраничная пагинация DRF, по 10 объектов на страницу.

## Запуск проекта

1. Создать виртуальное окружение:

```bash
python -m venv venv
```

2. Активировать его:

```bash
venv\Scripts\activate
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Выполнить миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Создать суперпользователя:

```bash
python manage.py createsuperuser
```

6. Запустить сервер:

```bash
python manage.py runserver
```

## Основные URL

- `POST /api/register/` - регистрация
- `GET /api/projects/` - список проектов пользователя
- `GET /api/tasks/` - список задач доступных проектов
- `GET /api/docs/swagger/` - Swagger UI
- `GET /api/docs/redoc/` - ReDoc
- `GET /api/schema/` - OpenAPI schema

## Чек-лист проверки в Swagger

1. Выполнить миграции, если они ещё не применялись:

```bash
python manage.py makemigrations
python manage.py migrate
```

2. Запустить сервер:

```bash
python manage.py runserver
```

3. Открыть Swagger:

```text
http://127.0.0.1:8000/api/docs/swagger/
```

4. Создать 3 пользователей через `POST /api/register/`: `owner`, `author`, `assignee`.

Пример тела запроса:

```json
{
  "username": "owner",
  "password": "owner12345",
  "first_name": "Owner",
  "last_name": "Test",
  "email": "owner@example.com"
}
```

5. Сохранить `id` пользователей из ответов Swagger. Дальше использовать именно эти `id`.

6. Нажать `Authorize` в Swagger и войти как `owner`.

7. Создать проект через `POST /api/projects/`.
Поле `members` принимает список `id` пользователей.

```json
{
  "name": "Проект 1",
  "description": "Тест через Swagger",
  "members": [2, 3]
}
```

8. Проверить `GET /api/projects/`.
Ожидаемо: владелец видит созданный проект.

9. Переключиться на пользователя `author` через `Authorize`.

10. Проверить `GET /api/projects/`.
Ожидаемо: `author` тоже видит проект, так как добавлен в участники.

11. Создать задачу через `POST /api/tasks/` как `author`.

```json
{
  "project": 1,
  "title": "Первая задача",
  "description": "Проверка ролей",
  "priority": "medium",
  "status": "todo",
  "deadline": "2026-04-30",
  "assignee": 3
}
```

Допустимые значения:

- `priority`: `low`, `medium`, `high`
- `status`: `todo`, `in_progress`, `done`

12. Проверить `GET /api/tasks/` как `author`.
Ожидаемо: задача отображается в списке.

13. Переключиться на `assignee`.

14. Проверить `GET /api/tasks/`.
Ожидаемо: задача видна исполнителю.

15. Как `assignee`, вызвать `PATCH /api/tasks/{task_id}/` и изменить только `status`.

```json
{
  "status": "in_progress"
}
```

Ожидаемо: `200 OK`.

16. Как `assignee`, попробовать изменить `title`.

```json
{
  "title": "Новое название"
}
```

Ожидаемо: ошибка, так как исполнителю разрешено менять только `status` и `priority`.

17. Переключиться на `author`.

18. Как `author`, вызвать `PATCH /api/tasks/{task_id}/` и изменить только `description`.

```json
{
  "description": "Автор обновил описание"
}
```

Ожидаемо: `200 OK`.

19. Как `author`, попробовать изменить `status` или `title`.
Ожидаемо: ошибка.

20. Как `author`, вызвать `DELETE /api/tasks/{task_id}/`.
Ожидаемо: удаление разрешено автору задачи.

21. Создать ещё одну задачу и войти как `owner`.

22. Как `owner`, вызвать `PATCH /api/tasks/{task_id}/` и изменить любые поля.
Ожидаемо: владельцу проекта это разрешено.

23. Проверить фильтры:

- `GET /api/tasks/?status=todo`
- `GET /api/tasks/?priority=high`
- `GET /api/tasks/?assignee={assignee_id}`
- `GET /api/tasks/?deadline_after=2026-04-01&deadline_before=2026-04-30`

24. Проверить сортировку:

- `GET /api/tasks/?ordering=deadline`

25. Проверить список пользователей:

- `GET /api/users/`

Ожидаемо: возвращаются пользователи, связанные с проектами текущего пользователя.

## Замечание

В текущем окружении не удалось запустить Python и применить миграции автоматически, поэтому код подготовлен вручную. После установки рабочего Python достаточно выполнить команды из раздела запуска.
