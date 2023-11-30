from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from polls.models import Question, Choice  # Question이라는 이름의 테이블을 import하기
from django.views.generic import ListView
from django.views.generic import DetailView


# Create your views here.

class IndexView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # 최근 생성된 5개의 질문을 반환한다
        queryset = Question.objects.order_by('-pub_date')[:5]
        print(queryset)  # Question에 데이터가 정상적으로 들어가 있는지 확인용
        return queryset

class DetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultView(DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# def vote(request,question_id):
#     question = get_object_or_404(Question,pk = question_id)
#     try:
#         selected_chocie = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls/detail.html',{
#             'question' : question,
#             'error_message' : "You didn't select a choice"
#         })
#     else:
#         selected_chocie.votes += 1
#         selected_chocie.save()
#         return redirect('polls:results')