# coding=utf-8


from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from apps.user.managers import UserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver


class User(AbstractBaseUser):

    ROLES = (
        ("1", "学生"),
        ("2", "教师"),
        ("3", "教务员"),
    )

    username = models.EmailField(verbose_name="邮箱", unique=True, null=False)
    number = models.CharField(max_length=15, verbose_name="学号", unique=True, null=True, blank=True)
    role = models.CharField(max_length=1, choices=ROLES, default=1, verbose_name="角色")
    name = models.CharField(max_length=30, verbose_name="姓名")
    address = models.CharField(max_length=100, verbose_name="居住地址", null=True, blank=True)
    birthday = models.DateField(null=True, verbose_name="出生年月", blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="是否激活", default=False)
    is_superuser = models.BooleanField(verbose_name="超级用户", default=False)
    is_admin = models.BooleanField(verbose_name="管理员", default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address

        return self.username

    def get_short_name(self):
        # The user is identified by their email address

        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always

        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always

        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff

        return self.is_admin

    def __str__(self):
        return self.name or self.username

    def __unicode__(self):
        if not self.nickname:
            return self.username
        return self.nickname

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户表'


class EmailValidate(models.Model):
    email = models.EmailField(verbose_name='邮箱')
    code = models.CharField(max_length=16, verbose_name='验证码')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


@receiver(pre_save, sender=User)
def comment_after(sender, instance, **kwargs):
    if instance.role == "3":
        instance.is_admin = True

    else:
        instance.is_admin = False
