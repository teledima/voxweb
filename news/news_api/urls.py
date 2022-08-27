from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.NewsList.as_view()),
]
