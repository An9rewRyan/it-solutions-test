# it-solutions-test

## Быстрый старт
> В случае запуска на windows в pycharm, поменяйте line separator c CRLF на LF в файле services/backend/entrypoint.sh
1. Создайте файлы .env и .env.db в соответствие с примерами *.example
2. Запустите сборку контейнера ```docker compose up --build```
3. Перейдите http://localhost:8000/api/docs на для ознакомления с доступным api