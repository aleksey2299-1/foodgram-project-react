## Проект Foodgram

Посмотреть рецепты и/или поделиться своими.

Есть возможность подписки на пользователей, добавление рецептов в избранное или в корзину.

Чтобы создать рецепт необходимо зарегистрироваться.

### Как запустить сайт:

Скачать docker-compose.production.yml

Установить docker: https://www.docker.com/get-started/

В терминале linux это можно сделать так:
````
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin 
````

В директории проекта создайте файл .env c данными:
````
POSTGRES_DB=<название db>
POSTGRES_USER=<имя пользователя для db>
POSTGRES_PASSWORD=<пароль пользователя для db>
DB_HOST=db # если поменять, то тогда нужно поменять название сервиса в docker-compose.production.yml
DB_PORT=5432 # это порт по умолчанию для db
SECRET_KEY=<SECRET_KEY в настройках django>
DEBUG=<True или False>
ALLOWED_HOSTS=<ваши адреса через пробел(пример:localhost 127.0.0.1 xxxx.com)>
````


Запустить Docker в директории с файлом(чтобы запустить в фоновом режиме добавьте флаг -d):
````
docker compose -f docker-compose.production.yml up
````
В терминале Linux могут потребоваться права суперпользователя:
````
sudo docker compose -f docker-compose.production.yml up
````
### Как начать?

Перейте по адресу localhost:8800/

### Доступ по Api

__Вся информация касательно api доступна на странице localhost:8800/api/docs/:__
