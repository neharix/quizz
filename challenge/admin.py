from django.contrib import admin

from .models import Answer, Challenge, Question, UserAnswer

admin.site.register(Answer)
admin.site.register(Challenge)
admin.site.register(UserAnswer)


@admin.register(Question)
class questionAdmin(admin.ModelAdmin):
    list_display = ["question", "id", "challenge", "point"]
