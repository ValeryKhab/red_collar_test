# Django REST API – Points
## **1. Установка и запуск**
### **Шаг 1. Клонировать репозиторий**
Склонируйте проект из репозитория (или скачайте архив):
```
git clone <URL_репозитория>
cd <папка_проекта>
```
### **Шаг 2. Установить зависимости**
Установите зависимости, указанные в requirements.txt:
```
pip install --upgrade pip
pip install -r requirements.txt
```
### **Шаг 3. Настроить переменные окружения**
На проекте используется СУБД Postgres. Для ее подключения создайте файл .env в корне проекта со следующим содержимым:
```
# Секретный ключ Django
SECRET_KEY=django-insecure

# Настройки PostgreSQL
DB_NAME=geo_test
DB_USER=<Ваше имя пользователя>
DB_PASSWORD=<Ваш пароль>
DB_HOST=127.0.0.1
DB_PORT=5432
```
Убедитесь, что в settings.py используется загрузка этих переменных через os.environ
### **Шаг 4. Создать базу данных**
В PostgreSQL создайте базу данных:
```
createdb geo_test
```
Или через psql:
```
psql -U <Ваше имя пользователя> -c "CREATE DATABASE geo_test;"
```
### **Шаг 5. Применить миграции**
```
python manage.py migrate
```
### **Шаг 6. Создать суперпользователя**
```
python manage.py createsuperuser
```
### **Шаг 7. Запустить сервер**
```
python manage.py runserver
```
API будет доступно по адресу: http://127.0.0.1:8000/
## **2. Админка**
Django admin: http://127.0.0.1:8000/admin/  
Используйте учётные данные суперпользователя, созданного на шаге 6
## **3. Описание проекта**
Backend-приложение на Django для работы с географическими точками на карте.
Приложение предоставляет REST API для:
- создания географических точек
- добавления сообщений к точкам
- поиска точек и связанных сообщений в заданном радиусе от координат
- аутентификации пользователей
### **Технологический стек**
- Python 3.10+
- Django 5.x
- Django REST Framework
- PostgreSQL
### **Архитектура проекта**
Проект построен по классической архитектуре Django проекта с разделением логики по приложениям:
- `accounts` - регистрация, вход и выход пользователей
- `points` - работа с гео-точками и сообщениями
- `geo` - основной конфигурационный модуль проекта
### **Аутентификация и авторизация**
В проекте реализована простая аутентификация с помощью токенов (`TokenAuthentication`), а также с помощью сессий для возможности проверки кода из браузера (`SessionAuthentication`).  
При регистрации и входе пользователю автоматически создаётся токен, который передаётся в заголовке Authorization:  

`Authorization: Token <token>`  

При выходе токен удаляется из базы.  
Для проверки приложения из браузера нужно раскомментировать следующую строку (52) в файле settings.py:  

`# "rest_framework.authentication.SessionAuthentication"`

### **Работа с геоданными**
В приложении используются следующие модели данных:

#### Point
- name - название точки
- description - описание точки
- latitude - широта
- longitude - долгота
- creator - пользователь, создавший точку
- created_at - дата создания
- updated_at - дата обновления

#### Message
- text - текст сообщения
- author - автор сообщения
- point - гео-точка, к которой относится сообщение
- created_at - дата создания
- updated_at - дата обновления

Поиск точек в заданном радиусе реализован с использованием формулы гаверсинуса. Так как сообщения привязаны к точкам, тут же находятся и сообщения.
Для каждой точки рассчитывается расстояние до заданных координат, и в результат включаются только точки, находящиеся в пределах указанного радиуса.  
Радиус задаётся в километрах.  
## **4. Основные эндпоинты API**
Базовый URL: /points/  
URL Аутентификации: /auth/
  
**Гео-точки**
| Метод  | URL                 | Описание                       |
| ------ | ------------------- | ------------------------------ |
| GET    | `/points/`          | Список точек                   |
| POST   | `/points/`          | Создание новой точки           |
| GET    | `/points/<id>/`     | Детали точки                   |
| PUT    | `/points/<id>/`     | Обновить точку                 |
| DELETE | `/points/<id>/`     | Удалить точку                  |
| GET    | `/points/search/`   | Поиск точек в заданном радиусе |

**Сообщения**
| Метод  | URL                                | Описание                           |
| ------ | ---------------------------------- | ---------------------------------- |
| GET    | `/points/<point_id>/messages/` | Список сообщений к заданной точке  |
| POST   | `/points/<point_id>/messages/` | Создать сообщение к заданной точке |
| GET    | `/points/messages/<id>/`       | Детали сообщения                   |
| PUT    | `/points/messages/<id>/`       | Изменить сообщение                 |                
| DELETE | `/points/messages/<id>/`       | Удалить сообщение                  |

**Аутентификация**
| Метод  | URL               | Описание    |
| ------ | ----------------- | ----------- |
| POST   | `/auth/register/` | Регистрация |
| POST   | `/auth/login/`    | Вход        |
| POST   | `/auth/logout/`   | Выход       |

## **4. Примеры запросов Postman**
Регистрация  
<img width="853" height="401" alt="image" src="https://github.com/user-attachments/assets/395b4101-3ab8-4159-98d5-6e1c0f13bef8" />  
Вход  
<img width="853" height="401" alt="image" src="https://github.com/user-attachments/assets/2b04e4da-1653-49b5-aa70-47f8aa2da051" />  
Просмотр точек (далее токен везде вставлен в header)  
<img width="853" height="696" alt="image" src="https://github.com/user-attachments/assets/9eba2e76-9bfc-4f91-b676-769c3b79a528" />  
Создание точки  
<img width="853" height="617" alt="image" src="https://github.com/user-attachments/assets/438ec6a6-bab2-41fb-8ae6-aff13a2aff16" />  
Просмотр сообщений к точке  
<img width="853" height="695" alt="image" src="https://github.com/user-attachments/assets/61742ca6-a82d-48a8-b34c-0d9ff0cd5c6f" />  
Создание своего сообщения  
<img width="853" height="478" alt="image" src="https://github.com/user-attachments/assets/fcca3698-009a-4526-96e4-3f3128036197" />  
Поиск точек с сообщениями в радиусе  
<img width="853" height="702" alt="image" src="https://github.com/user-attachments/assets/e14edfad-a801-46f2-b28e-1168693be189" />  
Изменение точки  
<img width="853" height="702" alt="image" src="https://github.com/user-attachments/assets/c229c63b-5d50-4f99-8b24-37364d05a3a2" />  
Попытка изменения не владельцем  
<img width="853" height="485" alt="image" src="https://github.com/user-attachments/assets/bdd6485e-e12a-4c15-9a41-4f6c95d1a225" />  
Доступ к страницам без авторизации  
<img width="853" height="447" alt="image" src="https://github.com/user-attachments/assets/e6d8ae6c-d4a8-450d-9455-db697b5a366e" />  
Выход  
<img width="853" height="447" alt="image" src="https://github.com/user-attachments/assets/4c7f5db0-4ee5-4cc3-9535-d02028f3605b" />  

## **5. Примеры запросов в браузере**
Просмотр и создание точек  
<img width="1430" height="708" alt="image" src="https://github.com/user-attachments/assets/96790137-4c0d-4a14-a1e8-6adab1a3b1ca" />  
Просмотр чужой точки  
<img width="1430" height="739" alt="image" src="https://github.com/user-attachments/assets/dc3c76e5-b7b7-4180-b7d3-9ee58c2ca43e" />  
Просмотр своей точки  
<img width="1430" height="766" alt="image" src="https://github.com/user-attachments/assets/131fa882-2e28-41ee-b36c-0c5b917bfa10" />  
Просмотр и создание сообщений к точке  
<img width="1207" height="717" alt="image" src="https://github.com/user-attachments/assets/ac841eb8-21ea-440b-87ae-7b20bfdee214" />  
Поиск по радиусу  
<img width="1207" height="763" alt="image" src="https://github.com/user-attachments/assets/3638a3d9-c704-46b5-8f4d-c7a7c6c9c634" />  
Просмотр своего сообщения  
<img width="1207" height="675" alt="image" src="https://github.com/user-attachments/assets/1e1e3af5-065d-4949-8018-88f4d60ac3d6" />  
Доступ без авторизации  
<img width="1207" height="435" alt="image" src="https://github.com/user-attachments/assets/59f36ab9-b44d-40d0-8828-dab68a559ebd" />  







