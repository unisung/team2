from django import forms
from Final.models import Question, Answer
from django import forms

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        labels = {
            'subject': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }



class TopicForm(forms.Form):
    num_topics = forms.IntegerField(label='토픽 수', min_value=1, max_value=9)
