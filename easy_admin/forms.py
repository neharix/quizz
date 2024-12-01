from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from challenge.models import Answer, Challenge, Complexity, Question

bootstrap_attr = {"class": "form-control my-2"}
bootstrap_for_textarea = {"class": "form-control my-2", "rows": "1"}


class ChallengeForm(forms.ModelForm):

    name = forms.CharField(label="Ady", widget=forms.TextInput(attrs=bootstrap_attr))
    date_start = forms.DateTimeField(
        label="Başlamaly wagty",
        widget=forms.DateTimeInput(attrs=bootstrap_attr, format="%d.%m.%Y %H:%M"),
    )
    date_finish = forms.DateTimeField(
        label="Gutarmaly wagty",
        widget=forms.DateTimeInput(attrs=bootstrap_attr, format="%d.%m.%Y %H:%M"),
    )
    time_for_event = forms.IntegerField(
        label="Test üçin berlen wagt", widget=forms.NumberInput(attrs=bootstrap_attr)
    )
    questions_count = forms.IntegerField(
        label="Soraglaryň sany", widget=forms.NumberInput(attrs=bootstrap_attr)
    )

    class Meta:
        model = Challenge
        fields = (
            "name",
            "date_start",
            "date_finish",
            "time_for_event",
            "questions_count",
        )


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Question
        fields = ("content", "challenge", "complexity")
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    is_true = forms.BooleanField(
        label="Jogap dogrymy?",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )

    class Meta:
        model = Answer
        fields = ("content", "question", "is_true")
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }
