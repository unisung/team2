from django.urls import path

from .views import base_views, question_views, answer_views, home_views, api_db, about_views, LDA_views, wordcloud_views, TSNE_views, LDA_topic

from django.urls import path

app_name = 'Final'

urlpatterns = [

    # T_SNE
    path('TSNE/', TSNE_views.tsne, name='TSNE'),

    # wordcloud
    path('wordcloud/', wordcloud_views.word, name='wordcloud'),
    
    # LDA
    path('lda_visualization/', LDA_topic.topic, name='lda_visualization'),
    path('lda_topic/', LDA_topic.topic, name='lda_topic'),

    # about-us
    path('about-us/', about_views.about, name='about-us'),

    # test
    path('test/', api_db.fetch, name='test'),

    # result
    path('result/', home_views.result, name='result'),
    path('download_csv/', home_views.download_csv, name='download_csv'),

    # home
    path('home/', home_views.home, name='home'),
    
    # base
    path('base/', base_views.index, name='base'),
    path('<int:question_id>/', base_views.detail, name='detail'),

    # question
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    # answer
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),
]
