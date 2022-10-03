from django.urls import path
from .views import dashboard, register_view, verify
urlpatterns = [
    path('', register_view, name='register_view'),
    path('verify/', verify, name='verify'),
    # path('login/', mobile_login, name='mobile_login'),
    path('dashboard/', dashboard, name='dashboard')
]