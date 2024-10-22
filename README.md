# Веб-приложение на Python с использованием FastAPI
## Стек технологий
1. python == 3.9
2. fastapi == 0.111.0
3. uvicorn == 0.30.1
4. starlette == 0.37.2
5. uvicorn == 0.30.1
6. sqlalchemy == 2.0.31
7. pydantic == 2.8.2
8. FastAPI-SQLAlchemy  == 0.2.1
9. python-dotenv == 1.0.1
10. pytest == 8.2.2
11. psycopg2 == 2.9.9
12. alembic == 1.13.2
13. python-multipart == 0.0.12
14. httpx == 0.27.2
15. psycopg2-binary == 2.9.10
## Функционал
1. GET/product: Получить список всех товаров
2. GET/product/{name}: Получить конкретный товар по его имени
3. GET/product/category/{category}: Получить товары по конкретной категории
4. GET/product/filtering/{initial_price}&{final_price}: Получить товары через фильтр цены
5. POST/product: Добавить новый товар
6. PUT/product/{name}: Обновить существующий товар
7. DELETE/product/{name}: Удалить товар
## Запуск
1. Склонировать репозиторий
2. Создать базу данных в PostgreSQL
```env
CREATE DATABASE {db_name};
```
3. Создать .env в папке src и записать следующие данные в нее
```env
DB_HOST = "host.docker.internal"
DB_PORT = "5432"
DB_NAME = {name}
DB_USER = {user}
DB_PASS = {pass}
```
4. Создать и запустить Docker 
```env
docker-compose up --build
```
5. Перейти по URL: http://localhost:8000/docs
6. Для запуска unit-тестов необходимо выполнить следующие
команды.
```env
 docker-compose exec pytest bash
 pytest
```