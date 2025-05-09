

### Использованные технологии:

В проекте использованы Python, selenium, unittest, mailslurp_client

### Как работать с mailslurp:

На сайте https://app.mailslurp.com зарегестрироваться и получить токен для почты.
В файле login_mail.py в переменной MAILSLURP_API_KEY сохранить свой токен.

### Как запустить проект:

Копировать репозиторий и перейти в него в командной строке:

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv venv
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Запустить проект командой:

```
python test_unitest.py
python3 test_unitest.py
```
