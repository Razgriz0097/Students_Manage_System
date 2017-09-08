# coding=utf-8

from django.shortcuts import render, redirect
from django.contrib import auth
from apps.course.models import CourseTeacher, StudentScore
from django.contrib.auth.decorators import login_required
from apps.user.models import User, EmailValidate
from django.core.mail import EmailMultiAlternatives
from Students_Manage import settings
import uuid


def send_active_email(email, code):
    if not email:
        return
    subject = u'<StudentManager>邮箱验证'
    text_content = 'This is an important message'
    from_email = settings.EMAIL_MY_NICKNAME + '<%s>' % (settings.EMAIL_HOST_USER,)
    html_content = u'<b>激活链接：</b><a href="http://%s/user/validator-email?' \
                   u'email=%s&code=%s">' \
                   u'点击进行邮箱验证</a>' % (settings.SERVER_HOST, email, code)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@login_required
def index(request):
    if request.user.role == "1":
        return render(request, "student_index.html")
    elif request.user.role == "2":
        course_list = [item.course for item in CourseTeacher.objects.filter(teacher=request.user)]
        return render(request, "teacher_index.html", {"course_list": course_list})


def user_login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if user.is_admin:  # 教务员等同于admin
                return redirect("/admin")
            return redirect("/")

        return redirect("/user/login")


@login_required
def user_logout(request):
    auth.logout(request)
    return redirect("/user/login")


@login_required
def user_edit(request):
    if request.method == "GET":
        return render(request, "student_edit.html")
    else:
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        user = request.user
        user.name = name
        user.mobile = mobile
        user.address = address
        user.save()
        return redirect("/")
    

@login_required
def user_query(request):
    if request.method == "GET":
        return render(request, "student_query.html")
    else:
        number = request.POST.get("number")
        student = User.objects.filter(number=number, role=1).first()
        return render(request, "student_query.html", {
            "name": student.name if student else "查询无此学生",
            "address": student.address if student else "查询无此学生",
            "mobile": student.mobile if student else "查询无此学生",
            "username": student.username if student else "查询无此学生",
            "number": student.number if student else "查询无此学生"
        })


def user_register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            User.objects.create_user(username=username, password=password, is_active=False)
        except Exception:
            return render(request, "system_info.html", {
                'msg': 'failed',
                'title': '错误',
                'content': '邮箱可能已经注册！',
                'url': ''
            })
        try:
            code = str(uuid.uuid4())[:16]
            verify_code = EmailValidate(email=username, code=code)
            verify_code.save()
            send_active_email(username, code)
            return render(request, "system_info.html", {
                'msg': 'success',
                'title': '恭喜',
                'content': '注册成功！请查看邮件进行验证。',
                'url': ''
            })
        except Exception:
            return render(request, "system_info.html", {
                'msg': 'failed',
                'title': '错误',
                'content': '邮件发送失败',
                'url': ''
            })


@login_required
def validator_email(request):
    email = request.GET.get('email', None)
    code = request.GET.get('code', None)
    item = EmailValidate.objects.filter(email=email, code=code).first()
    if item:
        user = User.objects.filter(username=email).first()
        if not user:
            data = {
                'msg': 'failed',
                'title': '出错啦',
                'content': '邮箱验证失败。',
                'url': '/user/register'
            }
            return render(request, "system_info.html", data)

        user.is_active = True
        user.save()
        item.delete()
        data = {
            'msg': 'success',
            'title': '恭喜',
            'content': '邮箱验证成功！即将跳转回到主页。',
            'url': '/user/login'
        }
        return render(request, "system_info.html", data)
    else:
        data = {
            'msg': 'failed',
            'title': '出错啦',
            'content': '邮箱未注册或已验证 即将跳转回到主页。',
            'url': '/'
        }
        return render(request, "system_info.html", data)


@login_required
def change_pwd(request):
    if request.method == "GET":
        return render(request, "change_pwd.html")
    else:
        new_pwd = request.POST.get("password")
        request.user.set_password(new_pwd)
        request.user.save()
        return redirect("/user/logout")


@login_required
def student_grade_query(request):
    if request.method == "GET":
        return render(request, "student_grade_query.html")
    else:
        number = request.POST.get("number")
        student = User.objects.filter(number=number, role=1).first()
        if not student:
            return render(request, "student_grade_query.html")
        all_score = StudentScore.objects.filter(student=student)
        return render(request, "student_grade_query.html", {
            "all_score": all_score
        })