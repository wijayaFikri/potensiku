from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from potensiku.questions import *
from potensiku.models import *
from potensiku.riasec_details import *
import json
from django.contrib.auth import authenticate, login, logout
from types import SimpleNamespace
import uuid
from django.db.models import Q


def login_backoffice(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if "nexturl" in request.session:
            nexturl = request.session.get("nexturl")
            del request.session["nexturl"]
            return redirect(nexturl)
        else:
            return redirect('back_office_index')

    else:
        return redirect('back_office_login')


def login_screen(request):
    if request.user.is_authenticated:
        return redirect('back_office_index')
    if request.GET.get('next') is not None:
        request.session["nexturl"] = request.GET.get('next')
    return render(request, 'potensiku_project/login.html')


@login_required(login_url='/backoffice/login')
def index(request):
    participant_list = []
    if request.GET.get("token") is not None:
        token = request.GET.get("token")
        fullname = request.GET.get("fullname")
        nip = request.GET.get("nip")
        query = Q()
        if token != "":
            query &= Q(token=token)
        if fullname != "":
            query &= Q(person__full_name__contains=fullname)
        if nip != "":
            query &= Q(person__nip=nip)
        query &= Q(done=True)
        participant_list = Participant.objects.filter(query)
    else:
        participant_list = list(Participant.objects.filter(done=True))
    participant_result_list = []
    for participant in participant_list:
        participant_result = ParticipantResult()
        participant_result.token = participant.token
        participant_result.name = participant.person.full_name
        participant_result.nip = participant.person.nip
        for answer in participant.answers.all():
            if answer.answer == 1:
                question = answer.question
                if question.category == "R":
                    participant_result.r += 1
                if question.category == "I":
                    participant_result.i += 1
                if question.category == "A":
                    participant_result.a += 1
                if question.category == "S":
                    participant_result.s += 1
                if question.category == "E":
                    participant_result.e += 1
                if question.category == "C":
                    participant_result.c += 1
        participant_result_list.append(participant_result)
    context = {
        "participants": participant_result_list,
    }
    return render(request, 'potensiku_project/index.html', context)


@login_required(login_url='/backoffice/login')
def participant_detail(request):
    token = request.POST.get("token")
    participant = Participant.objects.get(token=token)
    forms = build_detail_form()
    forms[0]["data"] = participant.person.full_name
    forms[1]["data"] = participant.person.nip
    forms[2]["data"] = participant.person.ttl
    forms[3]["data"] = participant.person.marriage_status
    forms[4]["data"] = participant.person.religion
    forms[5]["data"] = participant.person.address
    # pendidikan formal
    formal_education = []
    formal_education.append("SMA - " + participant.person.educationSMA)
    formal_education.append("D3 - " + participant.person.educationD3)
    formal_education.append("S1 - " + participant.person.educationS1)
    formal_education.append("S2 - " + participant.person.educationS2)
    formal_education.append("S3 - " + participant.person.educationS3)
    forms[6]["data"] = formal_education

    participant_result = calculate_answer(participant)
    test_result_array, test_result_detail = calculate_result(participant_result)
    test_result = ""
    for test_result_label in test_result_array:
        test_result = test_result + test_result_label + ", "
    test_result = test_result[:-2]
    # riwayat pengembangan
    self_improvement = [participant.person.history1, participant.person.history2, participant.person.history3]
    forms[7]["data"] = self_improvement

    context = {
        "form_data": forms,
        "result": participant_result,
        "test_result": test_result,
        "test_result_detail": test_result_detail
    }
    return render(request, 'potensiku_project/participant_detail.html', context)


@login_required(login_url='/backoffice/login')
def generate_token_screen(request):
    context = {}

    if request.GET.get("number_of_token") is not None:
        for i in range(int(request.GET.get("number_of_token"))):
            new_token_key = uuid.uuid4().hex[:9].upper()
            check_exist = Token.objects.filter(token=new_token_key).exists()
            while check_exist:
                new_token_key = uuid.uuid4().hex[:9].upper()
                check_exist = Token.objects.filter(token=new_token_key).exists()
            new_token = Token(token=new_token_key)
            new_token.save()
        context["message"] = request.GET.get("number_of_token") + " Token berhasil dibuat"

    tokens = list(Token.objects.all().order_by("-created_date"))
    context["tokens"] = tokens
    return render(request, 'potensiku_project/generate_token.html', context)


def calculate_answer(participant: Participant):
    participant_result = ParticipantResult()
    participant_result.token = participant.token
    participant_result.name = participant.person.full_name
    participant_result.nip = participant.person.nip
    for answer in participant.answers.all():
        if answer.answer == 1:
            question = answer.question
            if question.category == "R":
                participant_result.r += 1
            if question.category == "I":
                participant_result.i += 1
            if question.category == "A":
                participant_result.a += 1
            if question.category == "S":
                participant_result.s += 1
            if question.category == "E":
                participant_result.e += 1
            if question.category == "C":
                participant_result.c += 1
    return participant_result


def calculate_result(participant_result: ParticipantResult):
    test_result_detail = []
    test_result = []
    highest_result = 0
    if highest_result < participant_result.r:
        highest_result = participant_result.r
    if highest_result < participant_result.i:
        highest_result = participant_result.i
    if highest_result < participant_result.a:
        highest_result = participant_result.a
    if highest_result < participant_result.s:
        highest_result = participant_result.s
    if highest_result < participant_result.e:
        highest_result = participant_result.e
    if highest_result < participant_result.c:
        highest_result = participant_result.c

    if participant_result.r == highest_result:
        test_result_detail.append(get_riasec_for_r())
        test_result.append("Realistic")
    if participant_result.i == highest_result:
        test_result_detail.append(get_riasec_for_i())
        test_result.append("Investigative")
    if participant_result.a == highest_result:
        test_result_detail.append(get_riasec_for_a())
        test_result.append("Artistic")
    if participant_result.s == highest_result:
        test_result_detail.append(get_riasec_for_s())
        test_result.append("Social")
    if participant_result.e == highest_result:
        test_result_detail.append(get_riasec_for_e())
        test_result.append("Enterprising")
    if participant_result.c == highest_result:
        test_result_detail.append(get_riasec_for_c())
        test_result.append("Conventional")

    return test_result, test_result_detail


def logout_view(request):
    logout(request)
    return redirect('back_office_login')


def build_detail_form():
    form = [
        {
            "label": "Nama Lengkap",
            "type": "string"
        },
        {
            "label": "NIP",
            "type": "string"

        },
        {
            "label": "Tempat & Tanggal Lahir",
            "type": "string"
        },
        {
            "label": "Status Perkawinan",
            "type": "string"
        },
        {
            "label": "Agama",
            "type": "string"
        },
        {
            "label": "Alamat",
            "type": "string"
        },
        {
            "label": "Pendidikan Formal",
            "type": "list"
        },
        {
            "label": "Riwayat Pengembangan Kompetensi (seminar, diklat, kursus, penataran, atau magang)",
            "type": "list"
        },
    ]
    return form
