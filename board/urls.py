from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, ResponseCreate, \
    ResponseDelete, ResponseDetail, ResponsesList, response_approve, UserPosts

urlpatterns = [
    # список объявлений
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/response/create/', ResponseCreate.as_view(), name='response_add'), # отозваться на объявление
    path('response/<int:pk>', ResponseDetail.as_view(), name='response'),
    path('response/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
    path('response/<int:pk>/approve/', response_approve, name='response_accept'),
    # приватный список откликов на объявления пользователя
    path('response_list/', ResponsesList.as_view(), name='response_list'),
    # список объявлений пользователя в профиле - доступен и публично
    path('user_posts/<int:pk>', UserPosts.as_view(), name='user_posts'),
    ]

