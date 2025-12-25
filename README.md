# AskMe — инструкция по запуску

## Начало

Клонируйте репозиторий
```bash
git clone git@github.com:Saucesamba/AskMe.git
cd askme
```

## Запуск с Docker

1. Запустите демон Docker на своем компьютере.
2. Соберите и запустите сервисы:

```bash
docker-compose up -d --build
```
3. Проверьте, что контейнеры работают:

```bash
docker-compose ps
```
Должно быть запущено 3 контейнера

3. Установите зависимости в локальном venv (если будете запускать Django локально):

Запустить venv

powershell
```bash
.\.venv\Scripts\activate.ps1 
```
cmd
```cmd
.venv\Scripts\activate.bat
```

Установить зависимости
```bash
pip install -r requirements.txt
```

4. Сделать миграции БД:

```bash
python manage.py migrate
```

5. Создайте суперпользователя. Задайте ему логин и пароль.
  
```bash
python manage.py createsuperuser
```

6. Запустите приложение :

```bash
python manage.py runserver <host>:<port>
```
где вместо host и port укажите желаемый хост и порт. По умолчанию надо запускается с такой команды:
```bash
python manage.py runserver 127.0.0.1:5000
```

> Примечание: по умолчанию контейнер Postgres проброшен на порт **5433** (host: `localhost`, port: `5433`), Redis — **6379**, Centrifugo - **8035**

## Наполнение базы (тестовые данные)
Заполнить БД тестовыми данными можно так:

```bash
python manage.py fill_db [ratio]
```

Где `ratio` — коэффициент (например `1`, `10`) для масштабирования количества сущностей.

Пример команды: 
```bash
python manage.py fill_db --count 30
```


## Подключение внешних приложений
В файле  django.conf укажите конфигурацию для своих зависимостей
По умолчанию создастся следующее
- PostgreSQL:
  - host: `localhost`
  - port: `5433`
  - dbname: `askme_db`
  - user: `askme_user`
  - password: `askme_pass`
- Redis URL: `redis://localhost:6379/1`

- Redis
  - LOCATION = redis://localhost:6379/1
  - PREFIX = dz6
  - LIFETIME = 9660

- Centrifugo
  - ENABLED: True
  - HOST: http://localhost:8035/
  - URL: /centrifugo
  - API_KEY: RtYz5GoqVqJ5
  - SECRET: dRMmPyUZPXCb

## Запуск nginx 

1) Запустить приложение на доступном порту (у меня 5000)

```bash
gunicorn project.wsgi --bind 127.0.0.1:5000
```

2) настроить файл hosts добавив строку
127.0.0.1 askme.local

3) скопировать конфиг nginx (файл askme.conf) в папку nginx/conf

4) запустить nginx
```bash
.\nginx -c conf/askme.conf
```

5) перейти по адресу askme.local