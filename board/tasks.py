from datetime import timedelta

from allauth.account.models import EmailAddress
from celery import shared_task

from django.template.loader import render_to_string
from django.utils import timezone

from django.core.mail import send_mail
from .models import Author, Post


@shared_task
def periodic_mailing():
    # Создаем список рассылки из пользователей с подтвержденным email
    mail_list = []
    users = Author.objects.filter(is_subscriber=True)
    emails = EmailAddress.objects.filter(verified=True).values_list('user_id', 'email')
    for id, email in emails:
        username = users.get(author__id=id).username
        mail_list.append((username, email))

    # Проверяем наличие объявлений за прошедшие сутки и отправляем письма
    last_day = timezone.now() - timedelta(days=1)
    posts = Post.objects.filter(created__gte=last_day)
    if posts.exists():
        for subscriber in mail_list:
            html_content = render_to_string(
                'daily_mail.html',
                {
                    'link': 'http://127.0.0.1:8000',
                    'name': subscriber[0],
                    'posts': posts
                }
            )
            subject = f'{subscriber[0]}, новые объявления'
            send_mail(subscriber[1], subject, html_content)