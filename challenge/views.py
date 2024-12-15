import datetime
import json
import random

import pytz
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .containers import *
from .models import *
from .utils import *


def logout_view(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login_page")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        if request.POST.get("first_name", False) and request.POST.get(
            "last_name", False
        ):
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")

            username = remove_turkmen_letter(last_name.lower() + first_name.lower())

            if contains_cyrillic(username):
                username = transliterate(username)

            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    email="stub@mail.tm",
                    password=username + str(random.randint(1000000, 9999999)),
                    last_name=last_name,
                    first_name=first_name,
                )
                if request.POST.get("agency", False):
                    profile = Profile.objects.get(user=user)
                    profile.about = request.POST.get("agency")
                    profile.save()

            login(request, user)
            print(user.username)
            return redirect("home")

    context = {}
    return render(request, "views/login.html", context)


@login_required(login_url="/login/")
def index(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect("easy_tools")
        else:
            date = (
                datetime.datetime.now()
                .astimezone(pytz.timezone("Asia/Ashgabat"))
                .strftime("%Y-%m-%d %H:%M:%S")
            )
            challenges = Challenge.objects.filter(
                is_public=True, date_finish__gte=date, date_start__lte=date
            )
            available_challenges = []
            for challenge in challenges:
                if TestSession.objects.filter(
                    user=request.user, challenge=challenge
                ).exists():
                    test_session = TestSession.objects.get(
                        user=request.user, challenge=challenge
                    )
                    if test_session.end > datetime.datetime.now(
                        pytz.timezone("Asia/Ashgabat")
                    ):
                        available_challenges.append(challenge)
                else:
                    available_challenges.append(challenge)
            return render(
                request, "views/home.html", {"challenges": available_challenges}
            )
    return redirect("login_page")


@login_required(login_url="/login/")
def play_challenge(request: HttpRequest, challenge_id: int, question_id: int = None):
    if Challenge.objects.filter(id=challenge_id).exists():
        challenge = Challenge.objects.get(id=challenge_id)

    else:
        return redirect("home")

    if request.method == "POST":
        if request.POST.get("payload", False):
            payload = json.loads(request.POST["payload"])
            if payload.get("answer_id", False) and payload.get("question_id", False):
                question = Question.objects.get(id=payload["question_id"])
                if payload["answer_id"] != None:
                    answer = Answer.objects.get(id=payload["answer_id"])
                    is_true = True if answer.is_true else False
                    user_answer = UserAnswer.objects.create(
                        challenge=challenge,
                        question=question,
                        answer=answer,
                        is_true=is_true,
                        is_empty=False,
                        user=request.user,
                        answered_at=datetime.datetime.now().astimezone(
                            pytz.timezone("Asia/Ashgabat")
                        ),
                    )
                    if challenge.with_confirmation:
                        user_answer.confirmation = request.FILES.get("image", None)
                        user_answer.save()

                    test_session = TestSession.objects.get(
                        user=request.user, challenge=challenge
                    )
                    questions_sequence = json.loads(test_session.questions_json)
                    questions = [
                        QuestionContainer(question, request.user)
                        for question in Question.objects.filter(
                            id__in=questions_sequence
                        )
                    ]

                    prepositioned_questions = [None] * len(questions)
                    for q in questions:
                        prepositioned_questions[questions_sequence.index(q.id)] = q
                    questions = prepositioned_questions
                    del prepositioned_questions
                    # FIXME RESULT
                    question = None
                    for q in questions:
                        if not q.is_answered:
                            question = q
                            break

                    if question != None:
                        return redirect(
                            play_challenge,
                            challenge_id=challenge_id,
                            question_id=question.id,
                        )
                    else:
                        return redirect(results, challenge_id=challenge.id)

                return redirect(play_challenge, challenge_id=challenge_id)
            else:
                return redirect(play_challenge, challenge_id=challenge_id)
        else:
            return redirect(play_challenge, challenge_id=challenge_id)

    if TestSession.objects.filter(user=request.user, challenge=challenge).exists():
        test_session = TestSession.objects.get(user=request.user, challenge=challenge)
        if test_session.end.astimezone(
            pytz.timezone("Asia/Ashgabat")
        ) <= datetime.datetime.now(pytz.timezone("Asia/Ashgabat")):
            return redirect("home")
        else:
            questions_sequence = json.loads(test_session.questions_json)
            questions = [
                QuestionContainer(question, request.user)
                for question in Question.objects.filter(id__in=questions_sequence)
            ]

            prepositioned_questions = [None] * len(questions)
            for q in questions:
                prepositioned_questions[questions_sequence.index(q.id)] = q
            questions = prepositioned_questions
            del prepositioned_questions
            question = None

            if question_id == None:
                for q in questions:
                    if not q.is_answered:
                        question = q
                        break
            else:
                question = QuestionContainer(
                    Question.objects.get(id=question_id), request.user
                )

            # FIXME it means, that, a challenge haven't questions anymore
            if question == None:
                return redirect(results, challenge_id=challenge.id)
            # FIXME

            user_answers_count = UserAnswer.objects.filter(
                user=request.user, challenge=challenge
            ).count()

            answers = [
                ans
                for ans in Answer.objects.filter(
                    question=Question.objects.get(id=question.id)
                )
            ]
            random.shuffle(answers)

            return render(
                request,
                "views/challenge.html",
                {
                    "test_session": test_session,
                    "questions": questions,
                    "question": question,
                    "answers": answers,
                    "user_answers_count": user_answers_count,
                    "challenge": challenge,
                },
            )
    else:
        end = datetime.datetime.now(
            pytz.timezone("Asia/Ashgabat")
        ) + datetime.timedelta(minutes=challenge.time_for_event)

        share_of_questions = challenge.questions_count // 3
        rest_of_questions = challenge.questions_count % 3

        easy_temp = [
            question
            for question in Question.objects.filter(
                challenge=challenge, complexity=Complexity.objects.get(level="Ýeňil")
            )
        ]
        random.shuffle(easy_temp)
        medium_temp = [
            question
            for question in Question.objects.filter(
                challenge=challenge, complexity=Complexity.objects.get(level="Ortaça")
            )
        ]
        random.shuffle(medium_temp)
        hard_temp = [
            question
            for question in Question.objects.filter(
                challenge=challenge, complexity=Complexity.objects.get(level="Kyn")
            )
        ]
        random.shuffle(hard_temp)

        easy_questions = easy_temp[:share_of_questions]
        medium_questions = medium_temp[:share_of_questions]
        hard_questions = hard_temp[:share_of_questions]

        questions = easy_questions + medium_questions + hard_questions

        for i in range(rest_of_questions):
            questions.append(
                random.choice(
                    Question.objects.exclude(
                        pk__in=[question.pk for question in questions],
                    ).filter(challenge=challenge)
                )
            )

        test_session = TestSession.objects.create(
            user=request.user,
            challenge=challenge,
            end=end,
            questions_json=json.dumps([question.id for question in questions]),
        )

        question_containers = [
            QuestionContainer(question, request.user) for question in questions
        ]

        questions_sequence = json.loads(test_session.questions_json)
        questions = [
            QuestionContainer(question, request.user)
            for question in Question.objects.filter(id__in=questions_sequence)
        ]

        prepositioned_questions = [None] * len(questions)
        for q in questions:
            prepositioned_questions[questions_sequence.index(q.id)] = q
        questions = prepositioned_questions
        del prepositioned_questions

        if len(questions) > 0:
            question = questions[0]

        if question == None:
            return redirect(results, challenge_id=challenge.id)

        user_answers_count = UserAnswer.objects.filter(
            user=request.user, challenge=challenge
        ).count()

        answers = [
            ans
            for ans in Answer.objects.filter(
                question=Question.objects.get(id=question.id)
            )
        ]
        random.shuffle(answers)

        return render(
            request,
            "views/challenge.html",
            {
                "test_session": test_session,
                "questions": question_containers,
                "question": question,
                "answers": answers,
                "user_answers_count": user_answers_count,
                "challenge": challenge,
            },
        )


@login_required(login_url="/login/")
def confirmation(request: HttpRequest, challenge_id):
    if Challenge.objects.filter(id=challenge_id).exists():
        challenge = Challenge.objects.get(id=challenge_id)
    else:
        return redirect("home")

    if challenge.with_confirmation:
        if request.method == "POST":
            if request.FILES.get("image", False):
                ConfirmationImage.objects.create(
                    challenge=challenge, user=request.user, image=request.FILES["image"]
                )
                return redirect(play_challenge, challenge_id=challenge_id)
            return render(request, "views/confirmation.html")
        else:
            if ConfirmationImage.objects.filter(
                challenge=challenge, user=request.user
            ).exists():
                return redirect(play_challenge, challenge_id=challenge_id)
            else:
                return render(request, "views/confirmation.html")
    else:
        return redirect(play_challenge, challenge_id=challenge_id)


@login_required(login_url="/login/")
def timeout(request: HttpRequest, challenge_id: int, test_session_id: int):
    if Challenge.objects.filter(id=challenge_id).exists():
        challenge = Challenge.objects.get(id=challenge_id)
    else:
        return redirect("home")

    if TestSession.objects.filter(id=test_session_id).exists():
        test_session = TestSession.objects.get(id=test_session_id)
    else:
        return redirect("home")

    questions = Question.objects.filter(id__in=json.loads(test_session.questions_json))
    unanswered_questions = []
    for question in questions:
        if not UserAnswer.objects.filter(question=question, user=request.user).exists():
            unanswered_questions.append(question)
    for unanswered_question in unanswered_questions:
        UserAnswer.objects.create(
            challenge=challenge,
            question=unanswered_question,
            answer=None,
            is_true=False,
            is_empty=True,
            user=request.user,
            answered_at=datetime.datetime.now().astimezone(
                pytz.timezone("Asia/Ashgabat")
            ),
        )

    return redirect("home")


@login_required(login_url="/login/")
def change_question(request: HttpRequest, challenge_id: int, question_id: int):
    if Challenge.objects.filter(id=challenge_id).exists():
        challenge = Challenge.objects.get(id=challenge_id)
    else:
        return redirect("home")

    if Question.objects.filter(id=question_id).exists():
        return redirect(
            play_challenge, challenge_id=challenge_id, question_id=question_id
        )
    else:
        return redirect(play_challenge, challenge_id=challenge_id)


@login_required(login_url="/login/")
def results(request: HttpRequest, challenge_id: int):
    if Challenge.objects.filter(id=challenge_id).exists():
        challenge = Challenge.objects.get(id=challenge_id)
    else:
        return redirect("home")

    test_session = TestSession.objects.get(challenge=challenge, user=request.user)
    if test_session.end >= datetime.datetime.now().astimezone(
        pytz.timezone("Asia/Ashgabat")
    ):
        test_session.end = datetime.datetime.now().astimezone(
            pytz.timezone("Asia/Ashgabat")
        )
        test_session.save()
    user_answers = UserAnswer.objects.filter(user=request.user, challenge=challenge)
    user_result = UserResult(
        1,
        challenge.id,
        request.user,
        user_answers,
        test_session,
        True,
        challenge.questions_count,
    )
    return render(request, "views/results.html", {"user_result": user_result})
