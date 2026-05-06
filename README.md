# FastAPI Test Project

## Запуск проекта
ВАЖНО НЕ ЗАПУТАТЬСЯ С ПОРТАМИ, ПОТЕРЯЛ ВРЕМЯ И НЕРВЫ.

uvicorn main:app --reload --port 8000

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

