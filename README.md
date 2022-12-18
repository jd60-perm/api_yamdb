# API для YaMDb

### Описание проекта:

Учебный групповой проект. REST API для мини социальной сети YaMDb - портала отзывов на художественные произведения.
Проект еализован на фреймворке Django и встроенной в него БД sqlite с применением библиотеки Django REST framework.


### Системные требования: 

python 3.7


### Инструкция по развёртыванию:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/jd60-perm/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Загрузить тестовые данные:

```
python3 manage.py load_data
```

Запустить проект:

```
python yatube_api/manage.py runserver
```

![example workflow](https://github.com/jd60-perm/hw05_final/actions/workflows/main.yml/badge.svg)