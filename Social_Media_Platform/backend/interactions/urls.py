from django.urls import path
from .views import add_comment, toggle_like, toggle_follow

urlpatterns = [
    path(
        'comment/<int:post_id>/',
        add_comment,
        name='add_comment'
    ),

    path(
        'like/<int:post_id>/',
        toggle_like,
        name='toggle_like'
    ),

    path(
        'follow/<int:user_id>/',
        toggle_follow,
        name='toggle_follow'
    ),
]