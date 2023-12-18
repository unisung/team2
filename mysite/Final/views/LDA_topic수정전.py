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

from gensim import corpora

from tqdm import tqdm

import gensim
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
import json
import pickle
import base64
import time
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor


# 시간 단축 방법 
# 1. Word2Vec의 workers 매개변수를 조정하여 여러 코어를 사용하도록 설정할 수 있습니다.
# 2. LDA 모델 같은 경우, passes와 iterations 값이 클수록 학습에 더 많은 시간이 소요됩니다
# 3. 

# 실행 시간을 측정할 코드


def topic(request):
    start_time = time.perf_counter()

    context = {}
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')

        # 데이터베이스에서 검색
        items_from_db = Item.objects.filter(
            Q(astrtCont__icontains=keyword) | Q(inventionTitle__icontains=keyword)
        ).values_list('astrtCont', flat=True)
        # for q in items_from_db:
        #     print(q)
        #print(type(items_from_db))
        # 형태소 분석 및 DTM 생성
        mid_time1 = time.perf_counter()
        print(f"Time elapsed for first section: {int(round((mid_time1 - start_time) * 1000))}ms")
        
        kiwi = kiwipiepy.Kiwi()

        def extract_nouns(text):
            if text is None or not isinstance(text, str):
                return []  # 빈 리스트 반환 또는 적절한 기본값 설정
            stopwords = ['아', '휴', '아이구', '아이쿠', '아이고', '어', '나']  # 간소화된 불용어 리스트
            return [token.form for token in kiwi.tokenize(text) if token.tag in {'NNG', 'NNP'} and token.form not in stopwords]
        
        # 병렬 형태소 분석 처리 (추가됨)
        with ThreadPoolExecutor() as executor:
            docs_n = list(executor.map(extract_nouns, items_from_db))

        
        mid_time2 = time.perf_counter()
        print(f"Time elapsed for second section: {int(round((mid_time2 - start_time) * 1000))}ms")

        # ... (DTM 생성 및 docs_n 구성 코드 유지)
        cv = CountVectorizer(tokenizer=extract_nouns, min_df=10)
        #dtm = cv.fit_transform(items_from_db)  # 직접 items_from_db 사용


        mid_time3 = time.perf_counter()
        print(f"Time elapsed for third section: {int(round((mid_time3 - start_time) * 1000))}ms")

        # LDA 모델링 및 성능 평가
        noun_dic = corpora.Dictionary(docs_n)  # docs_n 사용
        noun_dic.filter_extremes(no_below=3, no_above=0.9)
        len(noun_dic)
        corpus = [noun_dic.doc2bow(doc) for doc in docs_n]  # docs_n 사용

        mid_time4 = time.perf_counter()
        print(f"Time elapsed for forth section: {int(round((mid_time4 - start_time) * 1000))}ms")

        # 사용자가 num_topics 입력한 경우 처리
        if 'num_topics' in request.POST:
            start_time = time.perf_counter()
            try:
                num_topics = int(request.POST['num_topics'])
                num_topics = max(num_topics, 1)  # 최소값을 1로 설정
                print('x')
                lda_model = LdaModel(corpus=corpus, num_topics=num_topics, id2word=noun_dic, passes=2, iterations=60, random_state=0)
                print('y')

                mid_time1_1 = time.perf_counter()
                print(f"Time elapsed for 1_1 section: {int(round((mid_time1_1 - start_time) * 1000))}ms")

                vis = pyLDAvis.gensim.prepare(lda_model, corpus, noun_dic)
                pyLDAvis_html = pyLDAvis.prepared_data_to_html(vis)
                print(pyLDAvis_html)  # 로그로 시각화 HTML 출력

                mid_time1_2 = time.perf_counter()
                print(f"Time elapsed for 1_2 section: {int(round((mid_time1_2 - start_time) * 1000))}ms")

                # 토픽별 주요 단어 추출
                topics = lda_model.print_topics(num_words=5)
                topics_str = [str(topic) for topic in topics]
                print(topics_str)

                mid_time1_3 = time.perf_counter()
                print(f"Time elapsed for 1_3 section: {int(round((mid_time1_3 - start_time) * 1000))}ms")

                return render(request, 'Final/lda_visualization.html', {'topics': topics_str, 'visualization': pyLDAvis_html})

                # context['visualization'] = pyLDAvis_html

                # 분석 결과 페이지로 리디렉션
                # return render(request, 'Final/lda_visualization.html', context)
            except ValueError:
                context['error'] = "토픽 수는 정수여야 합니다."

        context['keyword'] = keyword

        perplexity_score = []
        coherence_score = []
        for i in range(1, 10):
            ldamodel = LdaModel(corpus=corpus, num_topics=i, id2word=noun_dic, passes=2, iterations=60, random_state=0)
            perplexity = ldamodel.log_perplexity(corpus)
            perplexity_score.append(perplexity)
            coherence_model = CoherenceModel(model=ldamodel, texts=docs_n, dictionary=noun_dic, coherence='u_mass')
            coherence_score.append(coherence_model.get_coherence())

        mid_time5 = time.perf_counter()
        print(f"Time elapsed for fifth section: {int(round((mid_time5 - start_time) * 1000))}ms")

        context.update({
            'perplexity_data': json.dumps({
            'labels': list(range(1, 10)),
            'data': perplexity_score
            }),
                'coherence_data': json.dumps({
                    'labels': list(range(1, 10)),
                    'data': coherence_score
                })
            })
        context['keyword'] = keyword
        end_time = time.perf_counter()
        print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")

    return render(request, 'Final/lda_topic.html', context)
