from django.urls import path

from . import views 
app_name = "animals"

urlpatterns = [
	path('', views.index, name = 'index'),
	path('vote/',  views.vote, name = 'vote'),
	path('send', views.send_message, name = "send_message")
]