from django.apps import AppConfig

class GuestmodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guestmode'

	# 서버실행시 scheduler 실행
    def ready(self):
        from .expire import schedulerStart
        schedulerStart()
