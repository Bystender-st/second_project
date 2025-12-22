International Delivery Service API.

Backend-сервис для регистрации международных посылок, расчёта стоимости доставки и аналитики.



Установка и запуск.

 Предварительные требования

    -Docker
    -Docker Compose

 Клонирование репозитория
    git clone https://github.com/Bystender-st/second_project.git
    cd second_project

 Настройка окружения

    Создай файл .env в корне проекта:

        DATABASE_URL=mysql+aiomysql://appuser:apppass@mysql:3306/appdb
        REDIS_URL=redis://redis:6379/0
        SECRET_KEY=super-secret-key

    MongoDB подключается автоматически через Docker (mongodb://mongo:27017).


 Запуск проекта

    docker compose up -d --build


    После запуска API будет доступно по адресу:

        http://localhost:8000


 Swagger UI:

    http://localhost:8000/docs


 Аналитика

    Пример запроса:

        GET /analytics/daily-by-type?day=2025-12-21&tz_offset=+00:00


    Ответ:

        -тип посылки
        -количество
        -общая сумма доставок
        -средняя стоимость


 Запуск тестов:

    poetry install
    poetry run pytest


    В тестах:

        -используется SQLite
        -MongoDB и Redis отключены




Основные возможности.

 Работа с посылками

    -Регистрация посылок
    -Получение списка посылок с пагинацией
    -Получение посылки по ID
    -Расчёт стоимости доставки
    -Защита от повторного расчёта стоимости

 Сессии

    -Автоматическое управление session_id через cookies
    -Изоляция данных пользователей по сессиям
    -Хранение активных сессий в Redis

 Аналитика (MongoDB)

    -Хранение логов расчётов стоимости доставки
    -Подсчёт:
        количества посылок,
        общей суммы доставок,
        средней стоимости доставки
    -Агрегация по типам посылок за выбранный день
    -Поддержка таймзон через tz_offset

 Тестирование

    Полное покрытие ключевых API-сценариев
    Изолированная test-БД
    MongoDB и Redis отключаются в тестах




Используемые технологии

    -Python 3.12
    -FastAPI
    -SQLAlchemy 2.x (async)
    -MySQL 8
    -Redis 7
    -MongoDB 7 + Motor
    -Pydantic v2
    -Pytest + pytest-asyncio
    -Docker / Docker Compose
    -Poetry
    -Ruff, Mypy, Pre-commit
