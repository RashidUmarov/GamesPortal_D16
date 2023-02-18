"""GamesPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ckeditor_uploader.views import upload, browse
from django.views.decorators.cache import never_cache
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import LogoutView, LoginView, PasswordResetView, EmailVerificationSentView



# переопределим представления из allauth для того, чтобы прописать наши стили в шаблоны
class MyLogoutView(LogoutView):
    template_name = 'registration/logout.html'  # копия шаблога из allauth, только с нашим default.html. Ниже такие же операции


class MyLoginView(LoginView):
    template_name = 'registration/login.html'


class MyPasswordResetView(PasswordResetView):
    template_name = 'registration/password_change.html'


class MyEmailVerificationSentView(EmailVerificationSentView):
    template_name = 'registration/verification_sent.html'


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # подключаем встроенные эндопинты для работы с локализацией
    path('ckeditor/upload/', upload, name='ckeditor_upload'),
    path(r'ckeditor/browse/', never_cache(browse), name='ckeditor_browse'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),

    path('', lambda request: redirect('board/', permanent=False)),
    path("board/", include("board.urls"), name='board'),
    # блок переопределенных
    path('accounts/login/', MyLoginView.as_view(), name='account_login'),
    path('accounts/logout/', MyLogoutView.as_view(), name='account_logout'),
    path('accounts/email/', MyPasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/confirm-email/', MyPasswordResetView.as_view(), name='account_email_verification_sent'),
    path("accounts/", include("allauth.urls")),  # регистрация будет через allauth
    path("accounts/", include("accounts.urls")),  # а здесь работа с кастомным профилем
    path("board/", include("board.urls"), name='board'),
]
if settings.DEBUG:
    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
