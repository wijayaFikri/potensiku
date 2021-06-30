from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('store_answer', views.store_answer, name='store_answer'),
    path('start', views.start_fill_form, name='start_fill_form'),
    path('question', views.question_view, name='question'),
    path('register', views.register_participant, name='register')
]
