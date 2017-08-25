# -*- coding:utf-8 -*-

from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.

# 共用变量组，提供男女性选择
SEX_CHOICES = (
        (u'M', u'男性'),
        (u'F', u'女性'),
    )

class Students(AbstractUser):
    student_name = models.CharField(max_length=20, verbose_name=u'学生姓名')
    student_id = models.PositiveIntegerField(unique=True, verbose_name=u'学生学号')
    sex = models.CharField(max_length=2, choices=SEX_CHOICES, verbose_name=u'性别')
    mobile = models.CharField(max_length=11, verbose_name=u'手机号码')
    email = models.EmailField(verbose_name=u'邮箱')

    class Meta:
        verbose_name = u'学生'
        verbose_name_plural = verbose_name
        ordering = ['student_No']

    def __unicode__(self):
        return self.student_name

class Teachers(AbstractUser):
    teacher_name = models.CharField(max_length=20, verbose_name=u'教师姓名')
    teacher_id  = models.PositiveIntegerField(unique=True, verbose_name=u'教师编号')
    sex = models.CharField(max_length=2, choices=SEX_CHOICES, verbose_name=u'性别')
    mobile = models.CharField(max_length=11, verbose_name=u'手机号码')
    email = models.EmailField(verbose_name=u'邮箱')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name
        ordering = ['teacher_name']

    def __unicode__(self):
        return self.teacher_name

class Course(models.Model):
    course_name = models.CharField(max_length=40, verbose_name=u'课程名称')
    course_id = models.PositiveIntegerField(unique=True, verbose_name=u'课程代码')
    description = models.CharField(max_length=400, verbose_name=u'课程描述')
    teacher_id = models.ForeignKey(Teachers, verbose_name=u'任课教师')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name
        ordering = ['course_id']

    def __unicode__(self):
        return self.course_name

class Score(models.Model):
    student = models.ForeignKey(Students, verbose_name=u'学生')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    score = models.CharField(max_length=4, verbose_name=u'成绩')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name
        ordering = ['student']

