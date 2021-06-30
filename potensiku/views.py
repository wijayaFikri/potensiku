from django.shortcuts import render, HttpResponse, redirect
from potensiku.questions import *
from potensiku.models import *
import json
from types import SimpleNamespace


# Create your views here.
def index(request):
    if request.session.get("token") is not None:
        return redirect(start_fill_form)
    else:
        context = {
            "token": ""
        }
        return render(request, 'index.html')


def start_fill_form(request):
    if request.session.get("token") is not None:
        token_id = request.session.get("token")
    else:
        token_id = request.POST.get("token")
    token = Token.objects.filter(token=token_id).exists()
    if token:
        is_exist = Participant.objects.filter(token=token_id).exists()
        if is_exist:
            participant = Participant.objects.get(token=token_id)
            if participant is not None:
                request.session['token'] = participant.token
                return redirect(question_view)
        request.session['token'] = token_id
        return render(request, 'identity/index.html')
    else:
        context = {
            "error_message": "token tidak ditemukan , harap check kembali token anda",
            "token": token_id
        }
        return render(request, 'index.html', context)


def register_participant(request):
    person = Person(nip=request.POST.get("NIP"))
    person.full_name = request.POST.get("full_name")
    person.religion = request.POST.get("agama")
    person.ttl = request.POST.get("ttl")
    person.marriage_status = request.POST.get("status_perkawinan")
    person.religion = request.POST.get("agama")
    person.educationSMA = request.POST.get("pendidikanSma")
    person.educationD3 = request.POST.get("pendidikanD3")
    person.educationS1 = request.POST.get("pendidikanS1")
    person.educationS2 = request.POST.get("pendidikanS2")
    person.educationS3 = request.POST.get("pendidikanS3")
    person.title1 = request.POST.get("jabatanI")
    person.title2 = request.POST.get("jabatanII")
    person.title3 = request.POST.get("jabatanIII")
    person.history1 = request.POST.get("riwayatI")
    person.history2 = request.POST.get("riwayatII")
    person.history3 = request.POST.get("riwayatIII")
    person.achievement1 = request.POST.get("PenghargaanI")
    person.achievement2 = request.POST.get("PenghargaanII")
    person.achievement3 = request.POST.get("PenghargaanIII")
    person.save()
    participant = Participant(token=request.session.get("token"))
    participant.person = person
    participant.save()
    return redirect(question_view)


def question_view(request):
    for q in question_list:
        question = Question(id=q['id'], question=q['question'], category=['category'])
        question.save()

    context = {
        "questions": question_list,
    }
    token_id = request.session.get("token")
    participant = Participant.objects.get(token=token_id)
    answers = participant.answers.all()
    liste = list(answers)
    print(liste)
    return render(request, 'questions/index.html', context)


def store_answer(request):
    token_id = request.session.get("token")
    participant = Participant.objects.get(token=token_id)
    answer_target_exist = participant.answers.filter(question_id=request.POST.get("question_id")).exists()
    if answer_target_exist:
        old_answer = participant.answers.get(question_id=request.POST.get("question_id"))
        participant.answers.remove(old_answer)
        old_answer.delete()
    answer = Answer.objects.create(question_id=request.POST.get("question_id"), answer=request.POST.get("answer"))
    participant.answers.add(answer)
    list_answer = list(participant.answers.all())
    print(list_answer)
    if request.method == 'POST' and request.is_ajax():
        return HttpResponse(json.dumps({'name': "ok"}), content_type="application/json")
