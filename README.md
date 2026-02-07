# DjREST - Habits Tracker Backend

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение: \`python -m venv venv\`
3. Активируйте: \`source venv/bin/activate\`
4. Установите зависимости: \`pip install -r requirements.txt\`
5. Скопируйте .env.example в .env и настройте переменные
6. Выполните миграции: \`python manage.py migrate\`
7. Запустите сервер: \`python manage.py runserver\`

# Django-проект с Docker Compose

Этот проект демонстрирует, как запустить Django-приложение с PostgreSQL, Redis, Celery и Celery Beat с использованием Docker Compose.

## Предварительные требования

- Docker
- Docker Compose

## Инструкции по настройке

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <your-repo-url>
    cd DjREST
    ```

2.  **Создайте файл `.env`:**
    Скопируйте шаблон файла переменных окружения и заполните своими значениями.
    ```bash
    cp .env.example .env
    ```
    Отредактируйте `.env`, чтобы задать `SECRET_KEY`, `TELEGRAM_BOT_TOKEN` и другие параметры.

3.  **Соберите и запустите сервисы:**
    ```bash
    docker-compose up --build
    ```

4.  **Выполните миграции (в другом терминале):**
    После запуска контейнеров выполните:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Загрузите фикстуры (по желанию, в другом терминале):**
    ```bash
    docker-compose exec web python manage.py loaddata <название_фикстуры>.json
    ```

6.  **Создайте суперпользователя (в другом терминале):**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

## Как проверить статус сервисов

- **Django-приложение:** Перейдите по адресу `http://localhost:8000`
- **Логи Docker:** Выполните `docker-compose logs`, чтобы посмотреть логи всех сервисов.
- **PostgreSQL:** Слушает на `localhost:5432` (если нужен внешний доступ).
- **Redis:** Слушает на `localhost:6379` (если нужен внешний доступ).

## Остановка сервисов

Чтобы остановить и удалить контейнеры, сети и тома, созданные командой `up`, выполните:
    ```bash
        docker-compose down
    ```