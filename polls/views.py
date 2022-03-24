from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	
	def get_queryset(self):
		#Devuelve las cinco ultimas encuestas realizadas
		#Con objects.filter evitamos que se muestren las encuestas que estan con fechas futuras
		return Question.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		"""
		Excluye cualquier pregunta que no han sido publicadas aun
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

#Funcion de votacion
def vote(request, question_id):
    #Intentara encontrar el objeto y, encaso de de que no lo encuentre nos mostrara un error
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Volver a mostrar el formulario de votación de preguntas
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No has seleccionado una opción.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devuelva un HttpResponseRedirect después de manejar con
        # éxito los datos POST. Esto evita que los datos se publiquen dos 
        # veces si un usuario presiona el botón Atrás.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

"""Estas son las antiguas vistas que tenia aplicadas
#Muestra una plantilla con las cinco ultimas encuestas publicadas
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
"""
"""
#Funcion de detalles
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
"""
"""
#Funcion para ver los resultados
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""
