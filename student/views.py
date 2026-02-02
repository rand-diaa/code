from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce
from exam import models as QMODEL


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save(commit=False)
            user.set_password(userForm.cleaned_data['password'])
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    'total_course':QMODEL.Course.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    bundles=QMODEL.ExamBundle.objects.annotate(
        total_questions=Count('question', filter=Q(question__status='approved')),
        total_marks=Coalesce(Sum('question__marks', filter=Q(question__status='approved')), 0),
    )
    active_count = QMODEL.ExamBundle.objects.filter(is_active=True).count()
    return render(request,'student/student_exam.html',{'bundles':bundles,'active_count':active_count})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_start_exam_view(request,pk):
    bundle = QMODEL.ExamBundle.objects.get(id=pk, is_active=True)
    questions = QMODEL.Question.objects.filter(bundle=bundle, status='approved')
    return render(request,'student/student_start_exam.html',{'bundle':bundle,'questions':questions})
  