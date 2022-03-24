# Create your tests here.
"""Los test sirven para PREVENIR e IDENTIFICAR los fallos, MEJORAR el trabajo en equipo y hacer el codigo más atractivo"""

import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		"""Devolvera falso en caso de que la fecha de la pregunta sea del futuro """
		time = timezone.now() + datetime.timedelta(days=30)
		fut_question = Question(pub_date=time)
		self.assertIs(fut_question.was_published_recently(),False)

	def test_was_published_recently_with_old_question(self):
		"""Cuando la creación de la encuestas fue hace más de un día devolverá False"""
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(self))

	def test_was_published_recently_with_recent_question(self):
		"""Devolverá TRUE si la fecha de creación de la encuesta esta dentro del ultimo día"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(self))

	def create_question(question_text, days):
    		"""
    		Creamos una pregunta con el texto dado y publicado con el numero otorgado
    		"""
    		time = timezone.now() + datetime.timedelta(days=days)
    		return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):

    	def test_no_questions(self):
        	"""
        	Si no hay pregunta, se mostrará un mensaje en su lugar
        	"""
        	response = self.client.get(reverse('polls:index'))
        	self.assertEqual(response.status_code, 200)
        	self.assertContains(response, "No hay encuestas disponibles.")
        	self.assertQuerysetEqual(response.context['latest_question_list'], [])

    	def test_past_question(self):
        	"""
        	Preguntas con fechas pasadas serán mostradas
        	"""
        	question = create_question(question_text="Past question.", days=-30)
        	response = self.client.get(reverse('polls:index'))
        	self.assertQuerysetEqual(
        		response.context['latest_question_list'],
        		[question],
        	)

    	def test_future_question(self):
        	"""
        	Preguntas con fechas futuras no serán mostradas
        	"""
        	create_question(question_text="Future question.", days=30)
        	response = self.client.get(reverse('polls:index'))
        	self.assertContains(response, "No hay encuestas disponibles.")
        	self.assertQuerysetEqual(response.context['latest_question_list'], [])

    	def test_future_question_and_past_question(self):
        	"""
        	Aunque existan tanto preguntas con fechas futuras como con fechas del pasado, solo se mostrarán aquellas con fecha del pasado.
        	"""
        	question = create_question(question_text="Past question.", days=-30)
        	create_question(question_text="Future question.", days=30)
        	response = self.client.get(reverse('polls:index'))
        	self.assertQuerysetEqual(
        		response.context['latest_question_list'],
        		[question],
        	)

    	def test_two_past_questions(self):
        	"""
        	El indice mostrará diferentes preguntas
        	"""
        	question1 = create_question(question_text="Past question 1.", days=-30)
        	question2 = create_question(question_text="Past question 2.", days=-5)
        	response = self.client.get(reverse('polls:index'))
        	self.assertQuerysetEqual(
        		response.context['latest_question_list'],
        		[question2, question1],
        	)
class QuestionDetailViewTests(TestCase):

	def test_future_question(self):
        	"""
        	Los detalles de una pregunta en el futuro devolveran un 404 no encontrado
        	"""
        	future_question = create_question(question_text='Future question.', days=5)
        	url = reverse('polls:detail', args=(future_question.id,))
        	response = self.client.get(url)
        	self.assertEqual(response.status_code, 404)

	def test_past_question(self):
	        """
        	Los detalles de la pregunta con una fecha pasada mostraran el texto de la pregunta
        	"""
        	past_question = create_question(question_text='Past Question.', days=-5)
        	url = reverse('polls:detail', args=(past_question.id,))
        	response = self.client.get(url)
        	self.assertContains(response, past_question.question_text)
