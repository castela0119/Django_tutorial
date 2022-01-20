from tkinter.messagebox import RETRY
from django.forms import models
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

'''
request.POST 는 키로 전송된 자료에 접근할 수 있도록 해주는 사전과 같은 객체입니다. 
이 경우, request.POST['choice'] 는 선택된 설문의 ID를 문자열로 반환합니다. request.POST 의 값은 항상 문자열들입니다.

Django는 같은 방법으로 GET 자료에 접근하기 위해 request.GET 를 제공합니다 
그러나 POST 요청을 통해서만 자료가 수정되게하기 위해서, 명시적으로 코드에 request.POST 를 사용하고 있습니다.

만약 POST 자료에 choice 가 없으면, request.POST['choice'] 는 KeyError 가 일어납니다. 
위의 코드는 KeyError 를 체크하고, choice가 주어지지 않은 경우에는 에러 메시지와 함께 설문조사 폼을 다시보여줍니다.

설문지의 선택수가 증가한 이후에, 코드는 일반 HttpResponse 가 아닌 HttpResponseRedirect 를 반환하고, 
HttpResponseRedirect 는 하나의 인수를 받습니다: 그 인수는 사용자가 재전송될 URL 입니다.
(이 경우에 우리가 URL을 어떻게 구성하는지 다음 항목을 보세요).

위의 Python 주석에서 지적한 바와 같이 POST 데이터를 성공적으로 처리 한 후에는 '항상' HttpResponseRedirect 를 반환해야 합니다. 
이 팁은 Django에만 국한된 것이 아니라 일반적으로 좋은 웹 개발 관행입니다.

우리는 이 예제에서 HttpResponseRedirect 생성자 안에서 reverse() 함수를 사용하고 있습니다. 
이 함수는 뷰 함수에서 URL을 하드코딩하지 않도록 도와줍니다. 
제어를 전달하기 원하는 뷰의 이름을, URL패턴의 변수부분을 조합해서 해당 뷰를 가리킵니다. 
여기서 우리는 튜토리얼 3장에서 설정했던 URLconf를 사용하였으며, 이 reverse() 호출은 아래와 같은 문자열을 반환할 것입니다.

'/polls/3/results/'
'''