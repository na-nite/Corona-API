from django.conf.urls import url
from django.urls import path, include

from .views import (
    registration_view, login_visitor_view, login_staff_view,
    logout_view,
    user_detail_view, current_user_view, add_user_view,
    BlockUser, UnblockUser, UpdateUSer,
    DeleteUser, exchange_token)
from .admin_views import UserList

app_name = "user"

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/visitor/', login_visitor_view, name='login-visitor'),
    path('login/staff/', login_staff_view, name='login-staff'),
    path('logout/', logout_view, name='logout'),
    path('users/', UserList.as_view(), name='list-users'),
    path('user/<int:pk>', user_detail_view, name='user-detail'),
    path('current-user/', current_user_view, name='current-user'),
    path('add-user/', add_user_view, name='add-user'),
    path('update-user/<int:pk>', UpdateUSer.as_view(), name='update-user'),
    path('delete-user/<int:pk>', DeleteUser.as_view(), name='delete-user'),
    path('block-user/<int:pk>', BlockUser.as_view(), name='block_user'),
    path('unblock-user/<int:pk>', UnblockUser.as_view(), name='unblock_user'),
    url(r'social/(?P<backend>[^/]+)/$', exchange_token)
]
