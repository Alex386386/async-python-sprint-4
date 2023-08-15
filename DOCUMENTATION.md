# ЯП - Спринт 4 - Проект укоротителя ссылок реализованный на FastAPI.

### Описание

Запуская данный проект вам становится доступна возможность загружать в проект ссылки и получать укороченный вариант,
который будет переадресовывать вас на изначальную ссылку. Создавать ссылки могут только зарегистрированные пользователи.

### Установка, Как запустить проект:
https://github.com/Alex386386/async-python-sprint-4
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Alex386386/async-python-sprint-4
```

```
cd async-python-sprint-4
```

Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перед запуском приложения создайте базу данных для него используя следующую команду:

```
sudo docker run \
  --rm   \
  --name postgres-fastapi \
  -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=collection \
  -d postgres:14.5 
```

Запустите приложение следующй командой:

```
uvicorn app.main:app --reload
```

Документация по работе с проектом будет доступна по следующему адресу:

```
http://localhost:8000/docs
```

После запуска приложения, в базе данных автоматически будет создан суперюзер, логин и пароль от него можно найти в настройках.

Автор:
- [Александр Мамонов](https://github.com/Alex386386) 