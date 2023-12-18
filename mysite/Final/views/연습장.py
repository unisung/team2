import json

# ... [기타 필요한 임포트]

def lda_topic(request, keyword):
    if request.method == 'POST':
        # ... [키워드에 기반한 데이터베이스 검색 및 형태소 분석]

        # 퍼플렉시티와 일관성 점수 계산
        perplexity_score = []
        coherence_score = []
        for i in range(1, 10):
            ldamodel = LdaModel(corpus=corpus, num_topics=i, id2word=noun_dic, passes=2, iterations=60, random_state=0)
            perplexity = ldamodel.log_perplexity(corpus)
            perplexity_score.append(perplexity)
            coherence_model = CoherenceModel(model=ldamodel, texts=docs_n, dictionary=noun_dic, coherence='u_mass')
            coherence_score.append(coherence_model.get_coherence())

        # JSON 형식으로 데이터 변환
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

        return render(request, 'Final/lda_topic.html', context)

    return render(request, 'Final/lda_topic.html', {'keyword': keyword})
