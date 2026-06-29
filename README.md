# QA Auto Engineer Python Project

[![Hexlet check](https://github.com/anastaskanina1988-boop/qa-auto-engineer-python-project-314/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/anastaskanina1988-boop/qa-auto-engineer-python-project-314/actions/workflows/hexlet-check.yml)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4-43B02A?logo=selenium&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-9-0A9EDC?logo=pytest&logoColor=white)

Автотесты для учебного приложения Task Manager: React Admin доска задач с пользователями, статусами, метками и kanban-представлением.

## Что проверяется

- авторизация и выход из приложения;
- загрузка основных экранов админки;
- CRUD для пользователей, статусов, меток и задач;
- валидация email при создании пользователя;
- фильтрация задач по статусу, исполнителю и метке;
- отображение, сортировка, перемещение и удаление задач на kanban-доске.

## Требования

- Python 3.12+
- uv
- Docker
- Chrome и ChromeDriver

## Как поднять приложение

```bash
make start
```

Команда запускает Docker-контейнер с приложением на `http://localhost:5173`.

## Как запустить тесты

В отдельном терминале после запуска приложения:

```bash
make test
```

Отдельные сценарии авторизации:

```bash
make test-login
make test-logout
```

Можно запустить pytest напрямую:

```bash
APP_BASE_URL=http://localhost:5173 uv run pytest -v tests/
```
