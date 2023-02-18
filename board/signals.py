from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Response


@receiver(post_save, sender=Response)
def notify_response(sender, instance, created, **kwargs):
    # если отклика уже есть в базе, то сообщим автору отклика
    if created:
        subject = f'На ваше объявление "{instance.post.title}" поступил отклик {instance.created.strftime("%d %m %Y %H:%M")}'
        send_mail(subject='Для вашего объявления создан отклик!',
                  message=subject,
                  from_email=None,
                  recipient_list=[instance.post.author.author.email, ])
    elif instance.accepted:  # это только созданный отклик - напишем автору объявления
        subject = f'Ваш отклик на объявление "{instance.post.title}" одобрен автором {instance.created.strftime("%d %m %Y %H:%M")}'
        send_mail(subject='Ваш отклик на объявление одобрен!',
                  message=subject,
                  from_email=None,
                  recipient_list=[instance.user.email, ])
