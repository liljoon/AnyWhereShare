from django.urls import path
from account import views

# 계정관리
urlpatterns = [
    path('', views.ListAccountsView.as_view()),
    path('signup/', views.SignupView.as_view()),
    path('duplicate/', views.DuplicateView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    # path('hello/', views.HelloView.as_view()),
    path('delete/', views.WithdrawalView.as_view()),
    # path('modify/', views.modify_accounts),
    # path('<str:userId>', views.DetailAccountsView.as_view()),
]
