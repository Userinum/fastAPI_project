# FastAPI Test Project

## Запуск проекта

uvicorn main:app --reload

-------------------------------

## Запуск тестов

python3 -m pytest tests

-------------------------------

## Coverage

coverage run -m pytest tests
coverage html
open htmlcov/index.html

97%

-------------------------------

## Locust

cd tests
locust

