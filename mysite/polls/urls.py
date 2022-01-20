from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),

    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

'''
사용자가 웹사이트의 페이지를 요청할 때, 예로 《/polls/34/》를 요청했다고 하면, Django는 mysite.urls 파이썬 모듈을 불러오게 됩니다. ROOT_URLCONF 설정에 의해 해당 모듈을 바라보도록 지정되어 있기 때문입니다. 
mysite.urls에서 urlpatterns라는 변수를 찾고, 순서대로 패턴을 따라갑니다. 
'polls/'를 찾은 후엔, 일치하는 텍스트("polls/")를 버리고, 
남은 텍스트인 "34/"를 〈polls.urls〉 URLconf로 전달하여 남은 처리를 진행합니다. 
거기에 '<int:question_id>/'와 일치하여, 결과적으로 detail() 뷰 함수가 호출됩니다.
'''

'''
Django는 앱들의 URL을 어떻게 구별해 낼까요? 
예를 들어, polls 앱은 detail이라는 뷰를 가지고 있고, 동일한 프로젝트에 블로그를 위한 앱이 있을 수도 있습니다. 
Django가 {% url %} 템플릿태그를 사용할 때, 어떤 앱의 뷰(view)에서 URL을 생성할지 알 수 있을까요?

정답은 URLconf에 이름공간(namespace)을 추가하는 것입니다. 
polls/urls.py 파일에 app_name을 추가하여 어플리케이션의 이름공간을 설정할 수 있습니다.
'''