# 🎓 Edu Sphere (Платформа для онлайн-обучения)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-4.2-brightgreen)
![DRF](https://img.shields.io/badge/DRF-3.15-gray)
![Redis](https://img.shields.io/badge/Redis-5.1-red)
![Celery](https://img.shields.io/badge/Celery-5.4-green)

# Edu-sphere: LMS-система

🎓 **Edu-sphere** — это современная система управления обучением (LMS), разработанная с использованием мощных технологий Python и Django-REST-framework. Она предназначена для создания, распространения и управления образовательным контентом, а также для взаимодействия между студентами и преподавателями.

## Основные характеристики проекта:

- **RESTful API**: Используемый **Django REST Framework** обеспечивает создание гибкого и масштабируемого API для взаимодействия между клиентом и сервером.
- **Фильтрация данных**: С помощью **django-filter** легко фильтровать и сортировать данные на основе пользовательских запросов.
- **JWT-аутентификация**: Для безопасной аутентификации пользователей используется **djangorestframework-simplejwt**.
- **Документация API**: Интерактивная документация API реализована с помощью **drf-yasg**, что облегчает тестирование и использование API.
- **Оплата через Stripe**: Интеграция с **Stripe** позволяет легко настраивать и обрабатывать платежи за курсы и подписки.
- **Асинхронные задачи**: Используя **Celery** и **django-celery-beat**, система поддерживает выполнение фоновых задач, что повышает производительность и отзывчивость.
- **Кэширование**: Интеграция с **Redis** обеспечивает эффективное кэширование и обработку данных.

## 🛠️ Установка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/troxin-a/edu-sphere.git
cd edu-sphere
```

2. **Активируйте виртуальное окружение:**

```bash
poetry shell
```

3. **Установите зависимости:**

```bash
poetry install
```

4. **Создайте базу данных и примените миграции:**

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

5. **Создайте файл .env в корневом каталоге проекта и добавьте необходимые переменные окружения:**

```bash
cp .env.sample .env
nano .env
```

6. **Создайте группу модераторов приложение auth для создания необходимых групп пользователей:**

```bash
python3 manage.py fill
```

7. **Создайте суперпользователя:**

```bash
python3 manage.py csu
```

8. **Запустите локальный сервер:**

```bash
python3 manage.py runserver
```

9. **Запустите redis на локальной машине:**

```bash
redis-server
```

10. **Запустите celery + celery-beat:**

```bash
celery -A config worker --beat --scheduler django --loglevel=info
```

## 📚️ Использование
Документация по использованию API будет доступна после запуска сервера по ссылке: http://127.0.0.1:8000/redoc/

## Возможности

- 🎓 Управление курсами
- 👩‍🏫 Взаимодействие преподавателей и студентов
- 💳 Обработка платежей
