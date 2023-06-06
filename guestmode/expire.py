from apscheduler.schedulers.background import BackgroundScheduler
from .models import GuestUser
from django.utils import timezone
import datetime
from .s3_utils import deleteAllFiles

test = 1 # 테스트 상태일 경우 1로 설정하여 1시간동안 유효

# 생성된지 10분 지난 GuestUser 자동삭제
def expireGuestUser():
	expire_time = 10
	if test == 1:
		expire_time = 60 * 24
	users = GuestUser.objects.filter(create_at__lt = timezone.now() - datetime.timedelta(minutes=expire_time))
	if len(users) == 0:
		return
	for i in users:
		deleteAllFiles(i.passwd)
	print("Log : GuestUser Expired : " ,users.delete())

# 10초마다 삭제함수 실행
def schedulerStart():
	scheduler = BackgroundScheduler()
	scheduler.add_job(expireGuestUser, 'interval', seconds=10)
	scheduler.start()
