# Flask2_25052025

## Развертывание на локальной машине

1. Создаем виртуальное окружение: `python3 -m venv flask_venv`
2. Активируем venv: `source flask_venv/bin/activate`
3. Устанавливаем зависимости: `pip install -r requirements.txt`
4. Создаем локальную БД: `flask db upgrade`
5. Запускаем приложение: `python run.py`

## Ссылка на документацию
1. Настройки для запуска `flask run` [тут](https://flask.palletsprojects.com/en/stable/cli/)
2. Настройки для конфигов [тут](https://flask.palletsprojects.com/en/stable/config/)