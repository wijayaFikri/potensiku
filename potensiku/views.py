from django.shortcuts import render
from potensiku.questions import question_list


# Create your views here.
def index(request):
    return render(request, 'identity/index.html')


def question_view(request):
    participant_name = "edo"
    test_start_time = "aha"
    context = {
        "questions": question_list,
        "participant_name": participant_name,
        "test_start_time": test_start_time
    }
    return render(request, 'questions/index.html', context)
