from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.list_accounts),
    path('signup/', views.signup_accounts),
    # path('duplicate/', views.duplicate_accounts),
    # path('login/', views.login_accounts),
    # path('logout/', views.logout_accounts),
    # path('delete/', views.delete_accounts),
    # path('modify/', views.modify_accounts),
    path('<int:account_pk>', views.detail_accounts),
]