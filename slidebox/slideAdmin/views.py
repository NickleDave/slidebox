from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from .forms import *

import pdb

def index(request):
    template = loader.get_template('slideAdmin/index.html')
    return HttpResponse(template.render())

def addAnimal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/slidebox/') #goes back to index
    else:
        form = AnimalForm()
    return render(request, 'slideAdmin/addAnimal.html', {'form': form})

def addInject(request):
    if request.method == 'POST':
        form = InjectionForm(request.POST)
        if form.is_valid():
            form.save()          
            return HttpResponseRedirect('/slidebox/') #goes back to index
    else:
        form = InjectionForm()
    return render(request, 'slideAdmin/addInject.html', {'form': form})

def addResults(request): 
    if request.method == 'POST':
        form = ResultsForm(request.POST)
        
        if form.is_valid():
            form.save()

            if 'Save_and_add_another' in request.POST:
                animalID = form.cleaned_data.get('animalID', [])
                form = ResultsForm(initial={'animalID': animalID})
                return render(request, 'slideAdmin/addResults.html', {'form': form})

            elif 'Save_and_return' in request.POST:
                return HttpResponseRedirect(reverse('slideAdmin:index'))
    else: # not POST
        form = ResultsForm()
    return render(request, 'slideAdmin/addResults.html', {'form': form})

def searchAnimal(request):
    if request.method == 'GET' and request.GET:
        form = search_animal_form(request.GET)
        if form.is_valid():
            animal_results={}
            animal_results['animal_ID'] = \
                m.animalID.objects.filter(IDnumber=form.cleaned_data['animal_ID'])
            animal_results['injections'] = \
                m.injection.objects.filter(animalID=animal_results['animal_ID'])
            animal_results['inject_field_names'] = \
                [f.name for f in m.injection._meta.get_fields()]

            return render(request,'slideAdmin/search-animal-results.html',
                    {'animal_results':animal_results})
    else:
        form = search_animal_form()
    return render(request, 'slideAdmin/searchAnimal.html',{'form':form})

#def searchInject(request):
#    if request.method == 'GET' and request.GET:
#        form = search_inject_form(request.GET)
#        if form.is_valid():
#                cleaned_data = form.cleaned_data
#                return render(request, '
#    else:
#        form = search_inject_form()
#    return render(request, 'slideAdmin/searchInject.html')

def find_distance(request):
    #Django calls page with 'GET' the first time but Querydict is empty
    if request.method == 'GET' and request.GET:
        form = find_distance_form(request.GET)
        if form.is_valid():
            cleaned_data = form.measure()
            return render(request, 'slideAdmin/distance-results.html',
                {'cleaned_data':cleaned_data})
    else:
        form = find_distance_form()
    return render(request,'slideAdmin/FindDistance.html',{'form':form})

#def get_animalIDs(starts_with=''):
#    ID_list = []
#    if starts_wth:
#        ID_list = animalID.objects.filter(IDnumber__istartswith=starts_with)
#    return ID_list

#def suggest_animalID(request):
#    context = RequestContext(request)
#    ID_list = []
#    starts_with = ''
#    if request.method == 'GET'
#        starts_with = request.GET['suggestion']
