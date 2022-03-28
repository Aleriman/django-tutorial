from django.contrib import admin
# Register your models here.
#from .models import Question
from .models import Choice, Question
#Cambiamos admin.StackedInline por admin.TabularInline para reducir el tamaño que ocupan las 
#posibles respuestas a la pregunta
class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    #En la lista de cambios veremos los siguientes parametros: Pregunta, fecha publicacion y si
    #fue publicada recientemente
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    #fields = ['pub_date', 'question_text']
admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)

#admin.site.register(Question)
