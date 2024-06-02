from django.contrib import admin

from .models import Answer, Challenge, Question, UserAnswer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["answer", "id", "is_true", "question", "image"]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ["answer", "id", "is_true", "question", "user"]
    readonly_fields = ("answered_at",)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "id",
        "date_start",
        "date_finish",
        "time_for_event",
        "is_public",
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "id", "challenge", "point", "image"]
