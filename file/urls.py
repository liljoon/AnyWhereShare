from django.urls import path
from file import views

# 계정관리
urlpatterns = [
    # path('list/<path>', views.ListFilesView.as_view()),
    path('upload/', views.UploadView.as_view()),
    # path('download/<int:pk>', views.DownloadView.as_view()),
    # path('delete/<int:pk>', views.DeleteView.as_view()),
    # path('modify/<int:pk>', views.ModifyView.as_view()),
    # path('info/<int:pk>', views.InfoView.as_view()),
    # path('lock/<int:pk>', views.LockView.as_view()),
]
