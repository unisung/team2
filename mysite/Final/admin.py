from django.contrib import admin
from .models import Question, Item


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Item)