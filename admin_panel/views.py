from django.shortcuts import render,redirect
from . import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce
from exam import models
from teacher import models as TMODEL
from student import models as SMODEL
from django.contrib.auth.models import User


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

def admin_login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is admin (superuser or staff)
            if user.is_superuser or user.is_staff:
                login(request, user)
                return HttpResponseRedirect('afterlogin')
            else:
                return render(request, 'exam/adminlogin.html', {'error': 'You are not authorized as an administrator.'})
        else:
            return render(request, 'exam/adminlogin.html', {'error': 'Invalid username or password.'})
    return render(request, 'exam/adminlogin.html')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.filter(status='approved').count(),
    }
    return render(request,'exam/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    }
    return render(request,'exam/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')




@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'exam/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'exam/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student.html',{'students':students})



@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_exam_view(request):
    return render(request,'exam/admin_exam.html')


@login_required(login_url='adminlogin')
def admin_manage_exam_view(request):
    bundles = models.ExamBundle.objects.filter(status='approved')
    return render(request,'exam/admin_manage_exam.html',{'bundles':bundles})


@login_required(login_url='adminlogin')
def admin_start_exam_view(request,pk):
    bundle = models.ExamBundle.objects.get(id=pk)
    bundle.is_active = True
    bundle.save()
    return HttpResponseRedirect('/admin-manage-exam')


@login_required(login_url='adminlogin')
def admin_stop_exam_view(request,pk):
    bundle = models.ExamBundle.objects.get(id=pk)
    bundle.is_active = False
    bundle.save()
    return HttpResponseRedirect('/admin-manage-exam')



@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'exam/admin_question.html')


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    questions = models.Question.objects.select_related('course').filter(status='approved')
    return render(request,'exam/admin_view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def admin_view_pending_bundle_view(request):
    bundles = models.ExamBundle.objects.filter(status='pending')
    return render(request,'exam/admin_view_pending_bundle.html',{'bundles':bundles})

@login_required(login_url='adminlogin')
def admin_view_bundle_questions_view(request,pk):
    bundle = models.ExamBundle.objects.get(id=pk)
    questions = models.Question.objects.filter(bundle=bundle)
    return render(request,'exam/admin_view_bundle_questions.html',{'bundle':bundle,'questions':questions})

@login_required(login_url='adminlogin')
def approve_bundle_view(request,pk):
    bundle = models.ExamBundle.objects.get(id=pk)
    bundle.status = 'approved'
    bundle.save()
    models.Question.objects.filter(bundle=bundle).update(status='approved')
    return HttpResponseRedirect('/admin-view-pending-bundle')

@login_required(login_url='adminlogin')
def reject_bundle_view(request,pk):
    bundle = models.ExamBundle.objects.get(id=pk)
    bundle.delete()
    return HttpResponseRedirect('/admin-view-pending-bundle')

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'exam/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'exam/admin_check_marks.html',{'results':results})
