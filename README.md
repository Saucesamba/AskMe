### Для активации venv на Windows:




## Инструкция по запуску приложения

Клонировать репозиторий 

```powershell
git clone 
```

Активировать venv (Пример для Windows)

`.\.venv\Scripts\activate.ps1` - powershell

`.venv\Scripts\activate.bat` - cmd

Сделать миграции БД:

```Bash
python manage.py migrate
```

Выполнить скрипт для заполнения БД


```Bash
python manage.py fill_db [ratio]
```
Где num_users — коэффициент заполнения сущностей. Соответственно, после применения команды в базу должно быть добавлено:
 - пользователей — равное ratio;
 - вопросов — ratio * 10;
 - ответы — ratio * 100;
 - тэгов - ratio;
 - оценок пользователей - ratio * 200;


