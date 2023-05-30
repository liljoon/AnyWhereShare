from apscheduler.schedulers.background import BackgroundScheduler
from .models import GuestUser
from django.utils import timezone
import datetime
from .s3_utils import deleteAllFiles

# 생성된지 10분 지난 GuestUser 자동삭제
def expireGuestUser():
	users = GuestUser.objects.filter(create_at__lt = timezone.now() - datetime.timedelta(minutes=10))
	for i in users:
		deleteAllFiles(i.passwd)
	print("Log : GuestUser Expired : " ,users.delete())

# 10초마다 삭제함수 실행
def schedulerStart():
	scheduler = BackgroundScheduler()
	scheduler.add_job(expireGuestUser, 'interval', seconds=10)
	scheduler.start()
