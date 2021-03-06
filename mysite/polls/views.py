from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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
ListView와 DetailView의 두 가지 제너릭 뷰를 사용하고 있습니다. 
이 두보기는 각각 《개체 목록 표시》 및 《특정 개체 유형에 대한 세부 정보 페이지 표시》 개념을 추상화합니다.

각 제너릭 뷰는 어떤 모델이 적용될 것인지를 알아야합니다. 이것은 model 속성을 사용하여 제공됩니다.
DetailView 제너릭 뷰는 URL에서 캡처된 기본 키 값이 "pk"라고 기대하기 때문에 question_id를 제너릭 뷰를 위해 pk로 변경합니다.
기본적으로 DetailView 제너릭 뷰는 <app name>/<model name>_detail.html 템플릿을 사용합니다. 
우리의 경우에는 "polls/question_detail.html"템플릿을 사용할 것입니다. 
template_name 속성은 Django에게 자동 생성 된 기본 템플릿 이름 대신에 특정 템플릿 이름을 사용하도록 알려주기 위해 사용됩니다. results리스트 뷰에 대해서 template_name을 지정합니다 - 결과 뷰와 상세 뷰가 렌더링 될 때 서로 다른 모습을 갖도록합니다. 
이들이 둘다 동일한 DetailView를 사용하고 있더라도 말이지요.

마찬가지로, ListView 제네릭 뷰는 <app name>/<model name>_list.html 템플릿을 기본으로 사용합니다. 
이미 있는 "polls/index.html" 템플릿을 사용하기 위해 ListView 에 template_name 를 전달했습니다.

튜토리얼의 이전 부분에서 템플릿은 question 및 latest_question_list 컨텍스트 변수를 포함하는 컨텍스트와 함께 제공되었습니다. 
DetailView 의 경우 question 변수가 자동으로 제공되는데, 이는 우리가 Django 모델(Question)을 사용하고 있기 때문에 
Django가 컨텍스트 변수의 적절한 이름을 결정할 수 있습니다.

그러나 ListView의 경우 자동으로 생성되는 컨텍스트 변수는 question_list``입니다. 
이것을 덮어 쓰려면 ``context_object_name 속성을 제공하고, 대신에 latest_question_list 를 사용하도록 지정하십시오. 새로운 기본 컨텍스트 변수와 일치하도록 템플릿을 변경할 수도 있지만, 원하는 변수를 사용하도록 Django에게 지시하는 것이 훨씬 쉽습니다.
'''