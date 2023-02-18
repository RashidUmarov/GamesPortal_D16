
## Итоговое задание  "Доска объявлений"


### В рамках итогового задания D16 реализовано следующее:

-   Регистрация на сайте с подтверждением email
-   Фунционал по восстановлению пароля
-   Возможность публикации объявлений после потверждения почты
- Показ списка объявлений с пагинацией 
-  Редактирование и удаление только своих объявлений
- Подписка и отписка от новостей в своем профиле
-   Просмотр  своих объявлений и откликов на них в своем профиле
- Просмотр объявлений любого пользователя в его профиле
-   Авторизованные пользователи могут добавлять отклики на объявления
-   Отправка письма автору объявления после появления отклика
-   Одобрение и удаление откликов на свои объявления
-   Отправка письма автору отклика после его одобрения 
-   Ежесуточная рассылка пиьсма со списком новых объявлений только подписчикам


Для работы проекта необходимо установить  пакеты:
```
pip install django-bootstrap4

pip install django-allauth

pip install django-ckeditor

pip install celery

pip install redis

pip install -U "celery[redis]"

# - команда запуска Celery
celery -A MMORPG_board worker -l INFO -B 
```

requirements.txt:
```
python-dotenv==0.21.1
django-allauth==0.52.0
django-ckeditor==6.5.1
celery==5.2.7
redis==4.4.0
```