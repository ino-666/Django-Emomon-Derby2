from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager

class User(AbstractUser):
    money = models.IntegerField(default=300)  # 所持金
    # カスタムユーザーグループを定義します。関連名は"custom_user_set"です。
    groups = models.ManyToManyField(Group, blank=True, related_name="custom_user_set")
    # ユーザーのパーミッションを定義します。関連名は"custom_user_set"です。
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="custom_user_set") # type: ignore
    remaining_days = models.IntegerField(default=10) # レースまでの残りターン
    # EDが見れるかどうかを判断するフィールドです。
    ed_enables = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    # ユーザーの所持金を増やすメソッドです。
    def increase_money(self, increase_value):
        self.money += increase_value
        self.save()

    # EDを有効化するメソッドです。
    def enable_ending(self):
        self.ed_enables = True
        self.save()

class CustomUserManager(BaseUserManager):
    # カスタムユーザーを作成するメソッドです。
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

