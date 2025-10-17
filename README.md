# Course_5.

## Описание:

Проект Course_5 создан для отработки материалов по модулю DRF как курсовая работа онлайн школы SkyPro.

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/AlenaGuseva25/Course_5.git
```
2. Создайте файл .env в корне проекта на основе примера `.env.sample`

3. Запустите проект командой:
```
docker-compose up --build
```

4. После запуска выполните миграции:

```
docker-compose exec web python manage.py migrate
```
5. После запуска веб-приложение будет доступно по адресу: http://localhost:8001

## Настройка сервера и деплой приложения

1. Подготовка сервера (Ubuntu)
Установка Docker и Docker Compose
bash

- Обновление пакетов
sudo apt-get update

- Установка Docker
sudo apt-get install -y docker.io

- Установка Docker Compose
sudo apt-get install -y docker-compose

- Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker  # Применяем изменения без перезагрузки

- Проверка установки
docker --version
docker-compose --version
Остановка конфликтующих сервисов
bash
sudo systemctl stop postgresql redis nginx
sudo systemctl disable postgresql redis nginx

2. Настройка GitHub Actions
Добавьте секреты в репозиторий (Settings → Secrets → Actions):

* SSH_KEY — приватный ключ для доступа к серверу

* SERVER_IP — IP-адрес сервера

* SSH_USER — имя пользователя (обычно ubuntu)

* DEPLOY_DIR — путь для деплоя (например /home/ubuntu/app)

* DOCKER_HUB_USERNAME — логин Docker Hub

* DOCKER_HUB_ACCESS_TOKEN — токен Docker Hub

* Все переменные из .env.example

Workflow уже настроен в файле .github/workflows/ci.yml:

Автоматически запускается при push в main

Выполняет:

- Линтинг кода

- Тестирование

- Сборку Docker-образов

- Деплой на сервер

3. Ручной деплой (альтернатива CI/CD)
bash
- На сервере
git clone git@github.com:RadmilaGMTD/homework_drf.git
cd homework_drf

- Создайте .env файл с переменными окружения
nano .env

- Запустите приложение
docker-compose up -d --build

- Примените миграции
docker-compose exec homework_drf python manage.py migrate

- Создайте суперпользователя
docker-compose exec homework_drf python manage.py createsuperuser

4. Проверка работоспособности
API endpoints:

http://89.169.175.103/swagger/ — Swagger документация

5. Обновление приложения
При автоматическом деплое через GitHub Actions:

Сделайте push изменений в ветку main

Workflow автоматически развернет изменения

При ручном обновлении:

bash
git pull origin main
docker-compose down
docker-compose up -d --build

6. Важные команды
bash
- Остановка всех контейнеров
docker-compose down

- Просмотр запущенных контейнеров
docker-compose ps

- Пересборка конкретного сервиса
docker-compose up -d --build homework_drf

- Очистка системы Docker
docker system prune -a --volumes

## Проверка работоспособности сервисов

1. Django-приложение (web)
Откройте в браузере: http://localhost:8000/admin/

Войдите с данными суперпользователя

Убедитесь, что интерфейс администратора доступен

2. API endpoints
Получение списка курсов:
* Регистрация.(`users/create/`)
* Авторизация.(`users/token/`)


3. Celery worker
Проверьте логи Celery на выполнение задач:
```
docker-compose logs -f celery
```

4. PostgreSQL (db)
Подключитесь к БД для проверки:

```
docker-compose exec db psql -U your_db_user -d your_db_name
```

5. Redis
Проверьте подключение:

```
docker-compose exec redis redis-cli ping
```

Должен вернуться PONG

## Дополнительные команды:

Для просмотра запущенных контейнеров:

`docker-compose ps`

Для просмотра логов всех контейнеров:

`docker-compose logs`

Для остановки сервисов и удаления контейнеров:

`docker-compose down`



## Использование:

1. Откройте проект в среде программирования PyCharm или в VsCode.
2. Запустите python manage.py runserver и в postman можно посмотреть его работоспособность.

## Безопасность:

Все личные данные скрыты в файле .env, который скрыт от автокоммитов в репозиторий файлом 
.gitignore. Однако для удобства работы пример его заполнения есть в репозитории (.env.sample).
Все установленные зависимости есть в файле pyproject.toml. Так же настроен CORS.

## Реализация и функционал:

Проект реализует backend часть приложения для отслеживания привычек. В нем настроены модели привычки и авторизации. 
Модель привычки реализована и валидируется таким образом, чтобы нельзя было поставить время на выполнение привычки 
больше 120 секунд, нельзя сделать привычку публичное, если у нее нет признака хорошей привычки, а так же связанной может
быть только приятная привычка, так же если привычка приятная или уже связана с приятной привычкой нельзя выставить 
вознаграждение за ее выполнение. Помимо этого настроена отложенная задача для напоминания о привычке в телеграм 
пользователю, при этом нельзя зарегистрировать двух пользователей с одним и тем же телеграм id.
Реализован полный CRUD для привычки и авторизации, а так же через наследование от ReadOnlyModelViewSet ViewSet для 
опубликованных привычек исключительно для чтения. Увидеть их могут даже не авторизованные пользователи. 


## Тестирование:
Проект покрыт тестами, приложение авторизации пользователей протестировано косвенно через тестирование приложения
привычек.


## Документация:

Для получения дополнительной информации обратитесь к [документации](docs/README.md).

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).