from django.db import models

from student.models import Student
from teacher.models import Teacher
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   is_active = models.BooleanField(default=False)
   duration_minutes = models.PositiveIntegerField(default=60)
   per_question_seconds = models.PositiveIntegerField(default=60)
   def __str__(self):
        return self.course_name

class ExamBundle(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    )
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=False)
    duration_minutes = models.PositiveIntegerField(default=60)
    per_question_seconds = models.PositiveIntegerField(default=60)

    def __str__(self):
        return f"{self.title} ({self.course.course_name})"

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    bundle=models.ForeignKey(ExamBundle, on_delete=models.CASCADE, null=True, blank=True)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    QUESTION_TYPES = (
        ('mcq', 'Multiple Choice'),
        ('tf', 'True/False'),
    )
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='mcq')
    option1=models.CharField(max_length=200, blank=True)
    option2=models.CharField(max_length=200, blank=True)
    option3=models.CharField(max_length=200, blank=True)
    option4=models.CharField(max_length=200, blank=True)
    cat=(
        ('Option1','Option1'),
        ('Option2','Option2'),
        ('Option3','Option3'),
        ('Option4','Option4'),
        ('True','True'),
        ('False','False'),
    )
    answer=models.CharField(max_length=200,choices=cat)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')
    submitted_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

