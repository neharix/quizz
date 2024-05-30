from django.contrib import admin

from .models import Answer, Challenge, Question, UserAnswer

admin.site.register(Challenge)
admin.site.register(UserAnswer)


@admin.register(Answer)
class answerAdmin(admin.ModelAdmin):
    list_display = ["answer", "id", "is_true", "question"]


@admin.register(Question)
class questionAdmin(admin.ModelAdmin):
    list_display = ["question", "id", "challenge", "point"]
