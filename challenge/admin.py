from django.contrib import admin

from .models import (
    Answer,
    Challenge,
    Complexity,
    Profile,
    Question,
    TestSession,
    UserAnswer,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "about", "user"]
    readonly_fields = ("id",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "answer", "is_true", "question", "image", "is_image"]


@admin.register(Complexity)
class ComplexityAdmin(admin.ModelAdmin):
    list_display = ["id", "level"]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "answer", "is_true", "question", "user", "answered_at"]
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
    list_display = [
        "id",
        "question",
        "challenge",
        "point",
        "image",
        "is_image",
        "complexity",
    ]


@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display = ["id", "start", "end", "user", "challenge"]
    readonly_fields = ("start",)
