# coding=utf-8

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """通过邮箱，密码创建用户"""
    def create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError(u'用户必须要有用户名')
        user = self.model(username=username)
        user.set_password(password)
        user.is_active = True
        if kwargs:
            user.role = kwargs.get('role', 1)

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
