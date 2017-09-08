"""Students_Manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from apps.user.views import user_login, index, user_logout, user_edit, user_query, validator_email, \
    user_register, change_pwd, student_grade_query
from apps.course.views import teacher_course, change_grade, course_choose, student_choose_course, \
    student_unchoose_course

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^user/login$', user_login),
    url(r'^user/logout$', user_logout),
    url(r'^user/change-pwd$', change_pwd),
    url(r'^user/query$', user_query),
    url(r'^user/edit-info$', user_edit),
    url(r'^user/query/grade$', student_grade_query),
    url(r'^user/register$', user_register),
    url(r'^user/validator-email$', validator_email),
    url(r'^course/(\d+)$', teacher_course),
    url(r'^course/choose$', course_choose),
    url(r'^course/(\d+)/(\d+)/change-grade$', change_grade),
    url(r'^course/(\d+)/(\d+)/add$', student_choose_course),
    url(r'^course/(\d+)/(\d+)/delete$', student_unchoose_course),
]
