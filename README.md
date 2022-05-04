# :house: My pet-project: 'Flask wish list'
Этот проект был создан в целях изучения фреймворка Flask.

В данном проекте используется  :snake:`python 3.8`
- Для начала работы вам нужно создать виртуальное окружение 

  `python -m venv [name_dir]` - *создание виртуального окружения*

  `[name_dir]\Scripts\activate` -  *активирование виртуального окружения*

  и установить все зависимости.
  ```bash
    pip install -r requirements.txt
  ```
- Создайте католог `instance` внутри проекта, и в нутри него файл `config.py` со следующим содержимым.
  ```python
    #Flask_wishlist/instance/config.py
    from config import Config

    SECRET_KEY = "secret key for data base"
    SQLALCHEMY_DATABASE_URI = "your url database"
    UPLOAD_FOLDER = Config.UPLOAD_FOLDER
    IMG_FOLDER = Config.IMG_FOLDER
  ```
    я использовал в своем проекте *`Sqlite:`* `SQLALCHEMY_DATABASE_URI = "sqlite:///wishilist.db"`

- Теперь стоит инициализировать модели в бд и создать миграцию, используйте следующий набор команд в терминале.
  ```bash
    flask db init
  ```
  ```bash
    flask db migrate
  ```
  ```bash
    flask db upgrade
  ```

  при выполнение команд вам нужно находится в каталоге проекта 

  после чего у вас должен появиться файл *`wishlist.db`* в каталоге *`Flask_wishlist/app/`*
- Для запуска Flask приложения теперь стоит указать в переменную `FLASK_APP` наш файл `manage.py`

  это можно сделать через терминал написав команду `set FLASK_APP= menage.py`
  либо же можете создать файл `.flaskenv` и туда вписать эту переменную `FLASK_APP= manage.py`

- Запуск приложения

  вы можете использовать `flask run` либо же `python manage.py`
  
  
# :whale: Запуск приложения через Docker
- Если у вас уже установлен docker выполните следующую команду 
  ```bash
    docker run --name wishlist -d -p 8000:5000 --rm mikhailknyazev/wishlist
  ```
    теперь можете открыть [приложение](http://localhost:8000)
  
    если у вас еще не установлен docker то вам поможет официальная документация по установке на вашу OS
  
    можете пройти по следуйщей сылке --->  [docker install](https://docs.docker.com/engine/install/)

  
