from django.shortcuts import render, HttpResponse, redirect
from potensiku.questions import *
from potensiku.models import *
import json
from django.contrib.auth import authenticate
from types import SimpleNamespace


# Create your views here.
def index(request):
    if request.session.get("token") is not None:
        return redirect(start_fill_form)
    else:
        context = {}
        if "token_done_message" in request.session:
            context['error_message'] = request.session.get("token_done_message")
            del request.session['token_done_message']
        return render(request, 'index.html', context)


def temp_view(request):
    return render(request, 'sarah/participant_detail.html')


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
            if participant.done:
                request.session[
                    "token_done_message"] = "token tersebut telah digunakan dan sudah selesai mengerjakan test,mohon ganti token anda."
                return redirect('index')
            request.session['token'] = participant.token
            return redirect(question_view)
        new_token = Token.objects.get(token=token_id)
        new_token.is_used = True
        new_token.save()
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
    person.address = request.POST.get("address")
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
    context_list = get_question()

    token_id = request.session.get("token")
    participant = Participant.objects.get(token=token_id)
    answers = participant.answers.all()
    liste = list(answers)
    for question in context_list:
        for answer in liste:
            if answer.question_id == question["id"]:
                question["answer"] = answer.answer

    context = {
        "questions": context_list,
    }
    if request.session.get('confirm_error') is not None:
        context["error_message"] = request.session.get('confirm_error')
        del request.session['confirm_error']

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
    if request.method == 'POST' and request.is_ajax():
        return HttpResponse(json.dumps({'name': "ok"}), content_type="application/json")


def confirm(request):
    token_id = request.session.get("token")
    participant = Participant.objects.get(token=token_id)
    answers = participant.answers.all()
    liste = list(answers)
    if len(liste) < 42:
        request.session[
            'confirm_error'] = "System mendeteksi masih ada" \
                               " pertanyaan yang belum terjawab, mohon periksa kembali jawaban anda."
        return redirect('question')
    participant.done = True
    participant.save()
    request.session.flush()
    return render(request, 'finish/index.html')


def redirect_to_home(request):
    return redirect('index')
