from django.conf.urls import url
from . import views
from . import sarah_views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('store_answer', views.store_answer, name='store_answer'),
    path('start', views.start_fill_form, name='start_fill_form'),
    path('question', views.question_view, name='question'),
    path('register', views.register_participant, name='register'),
    path('confirm', views.confirm, name='confirm'),
    path('redirect', views.redirect_to_home, name='redirect'),
    path('sarah/login', sarah_views.login_screen, name='sarah_login'),
    path('sarah/authenticate', sarah_views.login_sarah, name='sarah_authenticate'),
    path('sarah/', sarah_views.index, name='sarah_index'),
    path('sarah/detail', sarah_views.participant_detail, name='participant_detail')
]
