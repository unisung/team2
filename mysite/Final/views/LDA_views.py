from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
import requests
import xmltodict
import pandas as pd
import time
import logging
from ..models import Item
import csv
from django.db.models import Q

from sklearn.feature_extraction.text import CountVectorizer
import pyLDAvis.gensim
import pyLDAvis
import kiwipiepy
from gensim.matutils import Sparse2Corpus
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary

from django.core.paginator import Paginator

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from gensim.models.coherencemodel import CoherenceModel
from gensim.models import LdaModel
import pickle
import base64

from django.shortcuts import render
from ..forms import TopicForm  # 가정한 폼 클래스 이름

def lda_visualization(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        # 세션에서 데이터 불러오기
        serialized_corpus = request.session.get('corpus')
        corpus = deserialize_corpus(serialized_corpus) if serialized_corpus else None

        serialized_noun_dic = request.session.get('noun_dic')
        noun_dic = deserialize_dictionary(serialized_noun_dic) if serialized_noun_dic else None

        serialized_docs_n = request.session.get('docs_n')
        docs_n = deserialize_dictionary(serialized_docs_n) if serialized_docs_n else None
        if form.is_valid():
            num_topics = form.cleaned_data['num_topics']  # 사용자 입력 받기
            lda_model = LdaModel(corpus, num_topics=num_topics, id2word=noun_dic, passes=3, iterations=100, random_state=0)
            vis = pyLDAvis.gensim.prepare(lda_model, corpus, noun_dic)
            pyLDAvis_html = pyLDAvis.prepared_data_to_html(vis)
            return render(request, 'Final/lda_visualization.html', {'visualization': pyLDAvis_html})
    else:
        form = TopicForm()  # GET 요청시 폼을 보여줌

    return render(request, 'Final/lda_visualization.html', {'form': form})



def deserialize_corpus(serialized_corpus):
    # Base64로 디코딩하고, Pickle로 역직렬화합니다.
    pickled_data = base64.b64decode(serialized_corpus)
    return pickle.loads(pickled_data)

def deserialize_dictionary(serialized_dictionary):
    # Base64로 디코딩하고, Pickle로 역직렬화합니다.
    pickled_data = base64.b64decode(serialized_dictionary)
    return pickle.loads(pickled_data)

def deserialize_dictionary(serialized_docs_n):
    # Base64로 디코딩하고, Pickle로 역직렬화합니다.
    pickled_data = base64.b64decode(serialized_docs_n)
    return pickle.loads(pickled_data)

# def lda_visualization(request):
#     if request.method == 'POST':
#         # 사용자가 입력한 토픽 수를 정수로 변환하고 검증
#         try:
#             num_topics = int(request.POST.get('num_topics', 1))
#             num_topics = max(num_topics, 1)  # 최소값을 1로 설정
#         except ValueError:
#             num_topics = 4  # 입력 값이 정수가 아닌 경우 기본값 설정
        
#         # 세션에서 데이터 불러오기
#         serialized_corpus = request.session.get('corpus')
#         corpus = deserialize_corpus(serialized_corpus) if serialized_corpus else None

#         serialized_noun_dic = request.session.get('noun_dic')
#         noun_dic = deserialize_dictionary(serialized_noun_dic) if serialized_noun_dic else None

#         serialized_docs_n = request.session.get('docs_n')
#         docs_n = deserialize_dictionary(serialized_docs_n) if serialized_docs_n else None

#         # LDA 모델 생성
#         lda_model = LdaModel(corpus, num_topics=num_topics, id2word=noun_dic, passes=3, iterations=100, random_state=0)

#         # 혼잡도와 일관성 점수 계산
#         if len(corpus) > 0:  # 분모가 0이 되는 것을 방지
#             perplexity = lda_model.log_perplexity(corpus)
#             if docs_n:
#                 coherence_model = CoherenceModel(model=lda_model, texts=docs_n, dictionary=noun_dic, coherence='u_mass')
#                 coherence = coherence_model.get_coherence()
#             # coherence_model = CoherenceModel(model=lda_model, texts=docs_n, dictionary=noun_dic, coherence='u_mass')
#             # coherence = coherence_model.get_coherence() if coherence_model.get_coherence() is not None else 0

#         # 토픽별 주요 단어 추출
#         topics = lda_model.print_topics(num_words=5)
#         topics_str = [str(topic) for topic in topics]

#         # 시각화
#         vis = pyLDAvis.gensim.prepare(lda_model, corpus, noun_dic)
#         pyLDAvis_html = pyLDAvis.prepared_data_to_html(vis)


#         return render(request, 'Final/lda_visualization.html', {
#             'topics': topics_str, 
#             'visualization': pyLDAvis_html,
#             'perplexity': perplexity, 
#             'coherence': coherence
#         })

#     return render(request, 'Final/lda_visualization.html')
