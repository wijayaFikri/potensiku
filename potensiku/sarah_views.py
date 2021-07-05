from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from potensiku.questions import *
from potensiku.models import *
import json
from django.contrib.auth import authenticate, login
from types import SimpleNamespace


def login_sarah(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('sarah_index')
    else:
        return redirect('sarah_login')


def login_screen(request):
    if request.user.is_authenticated:
        return redirect('sarah_index')
    return render(request, 'sarah/login.html')


@login_required(login_url='/sarah/login')
def index(request):
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
    return render(request, 'sarah/index.html', context)


@login_required(login_url='/sarah/login')
def participant_detail(request):
    token = request.POST.get("token")
    # token = "axby"
    participant = Participant.objects.get(token=token)
    forms = build_detail_form()
    databaru = ["data", "data", "data"]
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
    # rekam jejak jabatan
    position_history = []
    position_history.append(participant.person.title1)
    position_history.append(participant.person.title2)
    position_history.append(participant.person.title3)
    forms[7]["data"] = position_history
    # riwayat pengembangan
    self_improvement = [participant.person.history1, participant.person.history2, participant.person.history3]
    forms[8]["data"] = self_improvement
    # penghargaan
    achievements = [participant.person.achievement1, participant.person.achievement2, participant.person.achievement3]
    forms[9]["data"] = achievements

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

    context = {
        "form_data": forms,
        "result": participant_result
    }
    return render(request, 'sarah/participant_detail.html', context)


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
            "label": "Rekam Jejak Jabatan",
            "type": "list"

        },
        {
            "label": "Riwayat Pengembangan Kompetensi (seminar, diklat, kursus, penataran, atau magang)",
            "type": "list"
        },
        {
            "label": "Prestasi / Penghargaan",
            "type": "list"
        },
    ]
    return form