from django.urls import path
from file import views

# 계정관리
urlpatterns = [
    path('list/', views.ListFilesView.as_view()),
    path('upload/', views.UploadView.as_view()),
    path('newfolder/', views.NewFolderView.as_view()),
    path('download/', views.DownloadView.as_view()),
    path('delete/', views.DeleteView.as_view()),
    path('search/', views.SearchView.as_view()),
    path('info/', views.InfoView.as_view()),
    path('modify/', views.ModifyView.as_view()),
    path('trashlist/', views.ListTrashView.as_view()),
    path('recover/', views.RecoverView.as_view()),
    path('realdelete/', views.RealDeleteView.as_view()),
    # path('lock/', views.LockView.as_view()),
]
