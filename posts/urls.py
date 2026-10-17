from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.post_create, name="post_create"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("<int:pk>/like/", views.post_like, name="post_like"),
    path("<int:pk>/comment/", views.comment_add, name="comment_add"),
    path("<int:pk>/share/", views.post_share, name="post_share"),
    path("<int:pk>/delete/", views.post_delete, name="post_delete"),
]