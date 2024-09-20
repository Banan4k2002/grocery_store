# Магазин продуктов

Данный проект реализует тестовое задание для отдела бэкенд компании Сарафан.
Тестовое задание так же включало решение [задачи](/first_elements/).
Проект представляет собой backend для магазина продуктов с поддержкой следующего функционала:
- Управление продуктами, категориями и подкатегориями товаров через админку.
- Эндпоинты для получения списка категорий и продуктов с пагинацией.
- Функционал корзины для авторизованных пользователей с возможностью добавления, изменения, удаления товаров, очистки корзины и получения полного состава корзины.
- Авторизация по токену.
- Фикстуры для удобного наполнения данных.
- Поддержка документации API с помощью Swagger.
- Покрытие автотестами.

## Запуск проекта:

### 1. Клонируйте репозиторий:
`git clone https://github.com/Banan4k2002/grocery_store.git`

### 2. Cоздайте и активируйте виртуальное окружение:
Windows:
- `python -m venv venv`
- `source venv/Scripts/activate`

Linux/Mac:
- `python3 -m venv venv`
- `source venv/bin/activate`

### 3. Обновите пакетный менеджер и установите зависимости:
- `pip install --upgrade pip`
- `pip install -r requirements.txt`

### 4. Перейдите в директорию проекта:
`cd app/`

### 5. Запустите тесты:
`pytest`

### 6. Примените миграции:
`python manage.py migrate`

### 7. Создайте суперпользователя для доступа к админ-зоне:
`python manage.py createsuperuser`

### 8. Загрузите тестовые данные:
`python manage.py loaddata fixtures/products.json`

### 9. Запустите сервер разработки:
`python manage.py runserver`

## Документация API
Документация API доступна по адресу `http://127.0.0.1:8000/swagger/` после запуска проекта.

## Использованные технологии:
- Python 3.9
- Django 4.2.16
- Django REST Framework 3.15.2
- Djoser 2.2.3
- Drf-yasg 1.21.7
- Pytest 8.3.3
