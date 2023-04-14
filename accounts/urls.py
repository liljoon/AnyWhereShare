from django.urls import path
from . import views

urlpatterns = [
    # 계정관리
    path('', views.ListAccountsView.as_view()),
    path('signup/', views.SignupAccountsView.as_view()),
    path('duplicate/', views.DuplicateView.as_view()),
    path('login/', views.LoginAccountsView.as_view()),
    path('logout/', views.LogoutAccountsView.as_view()),
    path('hello/', views.HelloView.as_view()),
    # path('delete/', views.delete_accounts),
    # path('modify/', views.modify_accounts),
    path('<str:userId>', views.DetailAccountsView.as_view()),
]