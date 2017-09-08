# coding=utf-8

from django.shortcuts import render, redirect
from apps.course.models import Course, CourseStudent, StudentScore
from apps.user.models import User
from django.contrib.auth.decorators import login_required


@login_required
def teacher_course(request, cid):

    return render(request, "course_student.html", {
        "course": Course.objects.get(id=int(cid)),
        "students": list(CourseStudent.objects.get(course__id=int(cid)).student.all()),
    })


@login_required
def course_choose(request):
    choosed = [c.course for c in request.user.course.all()]
    for item in choosed:
        score_record = StudentScore.objects.filter(course=item, student=request.user).first()
        if score_record:
            setattr(item, "score", score_record.score)
        else:
            setattr(item, "score", "未出成绩")

    return render(request, "choose_course.html", {
        "choosed": choosed,
        "unchoosed": list(set(Course.objects.all()).difference(set(choosed))),
    })


@login_required
def change_grade(req, cid, sid):
    course = Course.objects.get(id=int(cid))
    student = User.objects.get(id=int(sid))
    score_record = StudentScore.objects.filter(course=course, student=student).first()
    if score_record:
        score = score_record.score
    else:
        score = 0
    if req.method == "GET":
        return render(req, "course_student_grade.html", {
            "score": score,
            "student": student.name,
            "course": course.name
        })
    else:
        score = float(req.POST.get("score", 0))
        score_record = StudentScore.objects.filter(student=student, course=course)
        if not score_record:
            score_record = StudentScore(student=student, course=course, score=score)
            score_record.save()
        else:
            score_record.score = score
            score_record

        return render(req, "course_student_grade.html", {
            "score": score,
            "student": student.name,
            "course": course.name
        })


def student_unchoose_course(request, cid, sid):
    course = Course.objects.get(id=int(cid))
    student = User.objects.get(id=int(sid))
    cs = CourseStudent.objects.get(course=course)
    cs.student.remove(student)
    cs.save()
    return redirect("/course/choose")


def student_choose_course(request, cid, sid):
    course = Course.objects.get(id=int(cid))
    student = User.objects.get(id=int(sid))
    cs = CourseStudent.objects.get(course=course)
    cs.student.add(student)
    cs.save()
    return redirect("/course/choose")