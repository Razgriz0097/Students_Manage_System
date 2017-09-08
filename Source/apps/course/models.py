# coding=utf-8


from django.db import models
from apps.user.models import User


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name="课程名称")
    desc = models.TextField(default="", verbose_name="课程简介", null=True, blank=True)
    enable = models.BooleanField(default=True, verbose_name="是否有效")

    class Meta:
        verbose_name = u'课程表'
        verbose_name_plural = u'课程表'

    def __str__(self):
        return self.name


class CourseStudent(models.Model):
    student = models.ManyToManyField(User, limit_choices_to={'role': 1}, verbose_name="选课学生", related_name="course")
    course = models.ForeignKey(Course, limit_choices_to={'enable': True}, verbose_name="课程")

    class Meta:
        verbose_name = u'学生选课关系表'
        verbose_name_plural = u'学生选课关系表'


class CourseTeacher(models.Model):
    teacher = models.ManyToManyField(User, limit_choices_to={'role': 2}, verbose_name="任课教师")
    course = models.ForeignKey(Course, limit_choices_to={'enable': True}, verbose_name="课程")

    class Meta:
        verbose_name = u'任课教师任课表'
        verbose_name_plural = u'任课教师任课表'


class StudentScore(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'role': 1}, verbose_name="学生")
    course = models.ForeignKey(Course, verbose_name="课程")
    score = models.FloatField(default=0, verbose_name="成绩")

    def __str__(self):
        return "%s %s %s" % (self.student, self.course, self.score)

    class Meta:
        verbose_name = u'学生成绩表'
        verbose_name_plural = u'学生成绩表'
