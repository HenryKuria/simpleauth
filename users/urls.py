from django.urls import path
from .views import AccessTokenCallback

app_name = 'users'

urlpatterns = [
    path('access-token-callback/', AccessTokenCallback.as_view(), name='access-token-callback'),
]
