from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('chatbot/', views.ChatBotView.as_view(), name='chatbot'),
]
