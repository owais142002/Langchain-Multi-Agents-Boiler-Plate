from django.urls import path
from . import views
from app.controllers.loginController import signup, validate_user
from app.controllers.aiController import chat

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('validate_user/', validate_user, name='validate_user'),
    path('chat/', chat, name="chat"),
]