import io

from django.contrib import admin
from django.core.management import call_command
from django.http import HttpResponse

from .models import *
from .utils import *


class UserAnswerAdmin(admin.ModelAdmin):
    actions = ["export_as_sql"]

    list_display = [
        "id",
        "answer",
        "is_true",
        "is_empty",
        "question",
        "user",
        "answered_at",
    ]
    readonly_fields = ("answered_at",)

    def export_as_sql(self, request, queryset):
        data = []
        for obj in queryset:
            model_data = {}
            for field in obj._meta.fields:
                value = getattr(obj, field.name)
                model_data[field.name] = value
            data.append(model_data)

        json_data = json.dumps(data, ensure_ascii=False, indent=4, default=json_encoder)

        table_name = "challenge__useranswer"
        sql_data = json_to_sql(json_data, table_name)

        response = HttpResponse(sql_data, content_type="application/sql")
        response["Content-Disposition"] = (
            f'attachment; filename="data-useranswers-{datetime.now().strftime("%d-%m-%Y")}.sql"'
        )
        return response

    export_as_sql.short_description = "SQL export"


admin.site.register(UserAnswer, UserAnswerAdmin)


class TestSessionAdmin(admin.ModelAdmin):
    actions = ["export_as_sql"]

    list_display = ["id", "start", "end", "user", "challenge"]
    readonly_fields = ("start",)

    def export_as_sql(self, request, queryset):
        data = []
        for obj in queryset:
            model_data = {}
            for field in obj._meta.fields:
                value = getattr(obj, field.name)
                model_data[field.name] = value
            data.append(model_data)

        json_data = json.dumps(data, ensure_ascii=False, indent=4, default=json_encoder)

        table_name = "challenge__testsession"
        sql_data = json_to_sql(json_data, table_name)

        response = HttpResponse(sql_data, content_type="application/sql")
        response["Content-Disposition"] = (
            f'attachment; filename="data-testsessions-{datetime.now().strftime("%d-%m-%Y")}.sql"'
        )
        return response

    export_as_sql.short_description = "SQL export"


admin.site.register(TestSession, TestSessionAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "about", "user"]
    readonly_fields = ("id",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "is_true", "question"]


@admin.register(Complexity)
class ComplexityAdmin(admin.ModelAdmin):
    list_display = ["id", "level"]


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
        "content",
        "challenge",
        "point",
        "complexity",
    ]


@admin.register(ConfirmationImage)
class ConfirmationImageAdmin(admin.ModelAdmin):
    list_display = ["user", "image", "date", "challenge"]
