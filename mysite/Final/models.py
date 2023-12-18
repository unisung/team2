from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Post(models.Model):
    postname = models.CharField(max_length=50)

    mainphoto = models.ImageField(blank=True, null=True)
    contents = models.TextField()

    def __str__(self):
        return self.postname
    
class Curriculum(models.Model):
    name = models.CharField(max_length=255)


### DB browser에 데이터 넣어보기

class Item(models.Model):
    
    applicantName = models.CharField(max_length=100, blank=True, null=True)  # 신청인 이름1
    applicationDate = models.CharField(max_length=8, blank=True, null=True)  # 신청 날짜, YYYYMMDD 형식2
    applicationNumber = models.CharField(max_length=20, blank=True, null=True)  # 신청 번호3
    astrtCont = models.TextField(blank=True, unique=True, null=True)  # 발명의 요약4
    bigDrawing = models.URLField(max_length=200, blank=True, null=True)  # 대형 도면 URL5
    drawing = models.URLField(max_length=200, blank=True, null=True)  # 도면 URL6
    indexNo = models.IntegerField(blank=True, null=True)  # 인덱스 번호7
    inventionTitle = models.CharField(max_length=200, blank=True, null=True)  # 발명의 제목8
    ipcNumber = models.CharField(max_length=100, blank=True, null=True)  # IPC 번호9
    openDate = models.CharField(max_length=100, blank=True, null=True) # 10
    openNumber = models.CharField(max_length=100, blank=True, null=True) # 11
    publicationDate = models.CharField(max_length=8, blank=True, null=True)  # 공개 날짜 12
    publicationNumber = models.CharField(max_length=100, blank=True, null=True) # 13
    registerDate = models.CharField(max_length=8, blank=True, null=True)  # 등록 날짜 14
    registerNumber = models.CharField(max_length=20, blank=True, null=True)  # 등록 번호 15
    registerStatus = models.CharField(max_length=50, blank=True,  null=True)  # 등록 상태 16


    def __str__(self):
        return self.invention_title
    