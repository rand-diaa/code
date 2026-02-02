from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from teacher import models as TMODEL
from student import models as SMODEL


def home_view(request):
    return render(request,'exam/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_teacher(request.user):
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')
    else:
        # Admin user (superuser or staff)
        return redirect('admin-dashboard')


def logout_view(request):
    """Custom logout view that accepts GET requests and redirects to homepage"""
    logout(request)
    return redirect('/')


