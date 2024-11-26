from django.contrib import admin

from .models import *

admin.site.register(AuthJournal)


@admin.register(ConfirmationImage)
class ConfirmationAdmin(admin.ModelAdmin):
    list_display = ["user", "pk", "date"]
    readonly_fields = ("date",)
