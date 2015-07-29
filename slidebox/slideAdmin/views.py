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


def FindDistance(request):
    if request.method == 'POST':
        form = FindDistanceForm(request.POST)
        if form.is_valid():
            measure_dict = form.measure()
            return HttpResponseRedirect(reverse('slideAdmin:index'))
    else: # if request.method == 'GET'
        form = FindDistanceForm()

    return render(request,'slideAdmin/FindDistance.html',{'form': form})
