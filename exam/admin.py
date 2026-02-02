from django.contrib import admin

from .models import Course, Question, Result


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "course_name")
    search_fields = ("course_name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "marks", "question", "answer")
    list_filter = ("course",)
    search_fields = ("question",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "exam", "marks", "date")
    list_filter = ("exam", "date")
