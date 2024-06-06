import datetime
from io import BytesIO

import pytz
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from docx import Document

from challenge.models import Challenge, Question, TestSession, UserAnswer

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
        session = TestSession.objects.get(challenge=challenge, user=user)
        now = datetime.datetime.now(datetime.timezone.utc)

        timezone = pytz.timezone("Asia/Ashgabat")
        if session.end > now.astimezone(timezone):
            is_finished = False
        else:
            is_finished = True

        pk += 1
        user_answers = []
        for question in questions:
            try:
                user_answers.append(
                    UserAnswer.objects.get(user=user, question=question)
                )
            except:
                pass
        user_results.append(
            UserResult(pk, challenge.pk, user, user_answers, session, is_finished)
        )
    return render(request, "challenge_result.html", {"users": user_results})


def side(request: HttpRequest):
    return render(request, "side.html")


def export_user_result_short(request: HttpRequest, challenge_id: int, user_id: int):

    challenge = Challenge.objects.get(pk=challenge_id)
    user = User.objects.get(pk=user_id)
    session = TestSession.objects.get(challenge=challenge, user=user)

    document = Document()

    questions = Question.objects.filter(challenge=challenge)

    user_answers = []
    for question in questions:
        try:
            user_answers.append(UserAnswer.objects.get(user=user, question=question))
        except:
            pass

    if len(user_answers) != 0:
        true_answer = sum([1 if answer.is_true else 0 for answer in user_answers])
        false_answer = sum([0 if answer.is_true else 1 for answer in user_answers])
        percent = round((true_answer / (true_answer + false_answer)) * 100)
    else:
        true_answer = 0
        false_answer = 0
        percent = 0

    start = session.start.strftime("%Y-%m-%d %H:%M:%S")
    end = session.end.strftime("%Y-%m-%d %H:%M:%S")

    document.add_heading(f'"{challenge.name}" testiň netijeleri', level=0)
    document.add_paragraph(f"Ady: {user.first_name}")
    document.add_paragraph(f"Familiýasy: {user.last_name}")
    document.add_paragraph(f"Başlan wagty: {start}")
    document.add_paragraph(f"Gutaran wagty: {end}")
    document.add_paragraph(f"Netije: {percent}")
    document.add_paragraph(f"Sorag sany: {true_answer + false_answer}")
    document.add_paragraph(f"Dogry jogaplaryň sany: {true_answer}")
    document.add_paragraph(f"Ýalňyş jogaplaryň sany: {false_answer}")

    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    return HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
