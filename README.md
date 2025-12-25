# AskMe — инструкция по запуску

## Требования
- Python 3.10+ (виртуальное окружение рекомендуется)
- Docker & Docker Compose (если хотите запускать Postgres/Redis в контейнерах)
- Git

## Быстрый запуск (Docker)
1. Соберите и запустите сервисы:

```powershell
docker-compose up -d --build
```

2. Проверьте, что контейнеры работают:

```powershell
docker-compose ps
```

3. Установите зависимости в локальном venv (если будете запускать Django локально):

`.\.venv\Scripts\activate.ps1` - powershell

`.venv\Scripts\activate.bat` - cmd

Сделать миграции БД:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

1. Запустите приложение :

```powershell
python manage.py runserver
```

> Примечание: по умолчанию контейнер Postgres проброшен на порт **5433** (host: `localhost`, port: `5433`), Redis — **6379**.

---

## Подключение внешних приложений
- PostgreSQL:
  - host: `localhost`
  - port: `5433`
  - dbname: `askme_db`
  - user: `askme_user`
  - password: `askme_pass`
- Redis URL: `redis://localhost:6379/1`


## Наполнение базы (тестовые данные)
Заполнить БД тестовыми данными можно так:

```powershell
python manage.py fill_db [ratio]
```

Где `ratio` — коэффициент (например `1`, `10`) для масштабирования количества сущностей.

## Запуск nginx 

1) Запустить приложение на доступном порту (у меня 5000)

```
gunicorn project.wsgi --bind 127.0.0.1:5000
```

2) настроить файл hosts добавив строку
127.0.0.1 askme.local

3) скопировать конфиг nginx в папку nginx
4) запустить nginx
```
.\nginx -c conf/askme.conf
```
6) перейти по адресу askme.local