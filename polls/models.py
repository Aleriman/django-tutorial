from django.db import models
from django.contrib import admin

import datetime

# Create your models here.
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Fecha de publicacion')
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def __str__(self):
        return self.question_text
    """Ahora las fechas a futuro darán falso ya que no son recientes"""
    def was_published_recently(self):
    	now = timezone.now()
    	return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
