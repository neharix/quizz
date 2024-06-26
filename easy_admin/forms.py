from django import forms

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

    class Meta:
        model = Challenge
        fields = ("name", "date_start", "date_finish", "time_for_event")


class QuestionForm(forms.ModelForm):
    question = forms.CharField(
        label="Sorag",
        widget=forms.Textarea(attrs=bootstrap_for_textarea),
        required=False,
    )
    image = forms.ImageField(
        label="Sorag", widget=forms.FileInput(attrs=bootstrap_attr), required=False
    )

    class Meta:
        model = Question
        fields = ("question", "image", "challenge", "complexity")


class AnswerForm(forms.ModelForm):
    answer = forms.CharField(
        label="Jogap",
        widget=forms.Textarea(attrs=bootstrap_for_textarea),
        required=False,
    )
    image = forms.ImageField(
        label="Jogap", widget=forms.FileInput(attrs=bootstrap_attr), required=False
    )
    is_true = forms.BooleanField(
        label="",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )

    class Meta:
        model = Answer
        fields = ("answer", "image", "question", "is_true")
