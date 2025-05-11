

### Использованные технологии:

В проекте использованы Python, selenium, unittest, mailslurp

### Как работать с mailslurp:

На сайте https://app.mailslurp.com зарегестрироваться и получить токен для почты.
В файле login_mail.py в переменной MAILSLURP_API_KEY сохранить свой токен. Для быстрой проверки можно использовать тот что указан в файле, но со временем он блокируется.

### Как запустить проект:

Копировать репозиторий и перейти в него в командной строке:

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Запустить проект командой:

```
python test_unitest.py
```
