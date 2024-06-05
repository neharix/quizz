from io import BytesIO

from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from docx import Document

from challenge.models import Challenge, Question, UserAnswer

from .response_fields import ChallengeResult, UserResult


def main(request: HttpRequest):
    users = User.objects.filter(is_superuser=False, is_staff=False)
    context = {"users": users}
    return render(request, "main.html", context)


def challenge_results(request: HttpRequest):
    challenges = Challenge.objects.all()
    challenge_results = []
    for index in range(len(challenges)):
        challenge_results.append(ChallengeResult(index + 1, challenges[index]))

    return render(request, "challenge_results.html", {"challenges": challenge_results})


def challenge_result(request: HttpRequest, challenge_id: int):
    challenge = Challenge.objects.get(pk=challenge_id)
    users = User.objects.filter(is_superuser=False, is_staff=False)
    questions = Question.objects.filter(challenge=challenge)

    user_results = []
    pk = 0
    for user in users:
        pk += 1
        user_answers = []
        for question in questions:
            user_answers.append(UserAnswer.objects.get(user=user, question=question))
        user_results.append(UserResult(pk, user, user_answers))
        print(user_results)
    return render(request, "challenge_result.html", {"users": user_results})


def side(request: HttpRequest):
    return render(request, "side.html")


def export_data_to_docx(request: HttpRequest):
    document = Document()

    # Add document title and heading
    document.add_heading("Data Export from Django", level=0)

    # Add table header row
    table = document.add_table(rows=1, cols=2)
    header_row = table.rows[0].cells
    header_row[0].text = "Field"
    header_row[1].text = "Value"

    # Save the document to a buffer
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    return HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
