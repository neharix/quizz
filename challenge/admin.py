from django.contrib import admin

from .models import Answer, Challenge, Question, UserAnswer

admin.site.register(Challenge)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["answer", "id", "is_true", "question"]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ["answer", "id", "is_true", "question", "user"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "id", "challenge", "point"]
