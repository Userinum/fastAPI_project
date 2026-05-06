# FastAPI Test Project

## Запуск проекта
ВАЖНО НЕ ЗАПУТАТЬСЯ С ПОРТАМИ, ПОТЕРЯЛ ВРЕМЯ И НЕРВЫ, КОГДА ЗАПУСКАЛ locust.

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
index.html - я закинул в репо

-------------------------------

## Locust

cd tests

locust

