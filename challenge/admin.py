from django.contrib import admin

from .models import Answer, Challenge, Question, UserAnswer

admin.site.register(Answer)
admin.site.register(Challenge)
admin.site.register(Question)
admin.site.register(UserAnswer)
