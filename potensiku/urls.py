from django.conf.urls import url
from . import views
from . import back_office_views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('store_answer', views.store_answer, name='store_answer'),
    path('start', views.start_fill_form, name='start_fill_form'),
    path('question', views.question_view, name='question'),
    path('register', views.register_participant, name='register'),
    path('confirm', views.confirm, name='confirm'),
    path('redirect', views.redirect_to_home, name='redirect'),
    path('backoffice/login', back_office_views.login_screen, name='back_office_login'),
    path('backoffice/authenticate', back_office_views.login_backoffice, name='back_office_authenticate'),
    path('backoffice/', back_office_views.index, name='back_office_index'),
    path('backoffice/detail', back_office_views.participant_detail, name='participant_detail'),
    path('backoffice/generate/token', back_office_views.generate_token_screen, name='generate_token'),
    path('backoffice/logout', back_office_views.logout_view, name='back_office_logout'),
]
