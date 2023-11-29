from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from polls.models import Question, Choice  # Question이라는 이름의 테이블을 import하기
from polls.forms import NameForm

# Create your views here.

def index(request):
    lastest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'lastest_question_list' : lastest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # 설문 투표 폼을 다시 보여 준다.
        return render(request, 'polls/detail.html',
                      {'question':question, 'error_message': "You didn't select a choice",})
    else:
        selected_choice.votes += 1
        selected_choice.save() # DB에 저장
        # POST 데이터를 정상적으로 처리하였으면,
        # 항상 HttpResponseRedirect를 반환하여 리다이렉션을 처리함
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid(): # 폼에 담긴 데이터가 유효한지 체크
            new_name = form.cleaned_data['name']
            return HttpResponseRedirect('')
    else:
        form = NameForm()
    return render(request, 'polls/name.html', {'form':form})


# -------------------



