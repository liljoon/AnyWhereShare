from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# 헬퍼 클래스
class UserManager(BaseUserManager):
    def create_user(self, userId, password, username, email, **kwargs):
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not userId:
            raise ValueError('Users must have an user id')

        if not password:
            raise ValueError('Users must have a password')

        if not username:
            raise ValueError('Users must have an username')

        if not email:
            raise ValueError('Users must have an email')
        user = self.model(
            userId=userId,
            password=password,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여
        """
        superuser = self.create_user(
            email=email,
            password=password,
        )

        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.save(using=self._db)
        return superuser


# AbstractBaseUser를 상속해서 유저 커스텀
class Account(AbstractBaseUser, PermissionsMixin):
    accountTypes = [
        ('RE', 'regular'),
        ('GU', 'guest'),
    ]
    userId = models.CharField(max_length=20, primary_key=True, unique=True, null=False)
    password = models.TextField(null=False)
    username = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    url = models.CharField(max_length=100, null=True)
    expirationTime = models.IntegerField(null=True)
    acountType = models.CharField(max_length=2, choices=accountTypes, default='RE')
    is_superuser = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=True, null=True)
    is_staff = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 email으로 설정 (이메일로 로그인)
    USERNAME_FIELD = 'userId'