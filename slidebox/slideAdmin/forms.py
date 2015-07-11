from django import forms
from django.forms import TextInput
from django.core.exceptions import NON_FIELD_ERRORS

from slideAdmin import models as m

import pdb

class InlineModelChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = kwargs.pop('widget', forms.widgets.TextInput)
        super(InlineModelChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and not self.required:
            return None
        try:
            return self.queryset.filter(IDnumber=value).get()
        except self.queryset.model.DoesNotExist:
            raise forms.ValidationError("Please enter a valid %s." % (self.queryset.model._meta.verbose_name,))

class AnimalForm(forms.ModelForm):
    class Meta:
        model = m.animalID
        fields = ['IDnumber',
        'surgeryDate',
        'surgeryNotebook',
        'surgeryNotebookPage',
        'perfusionDate',
        'sectionDate',
        'sectionThickness',
        'sectionPlane',]
        widgets = {
            'surgeryNotebook': forms.NumberInput(attrs={'min': 1}),
            'surgeryNotebookPage': forms.NumberInput(attrs={'min': 1}),
        }

class InjectionForm(forms.ModelForm):
    animalID = InlineModelChoiceField(queryset=m.animalID.objects.all())

    class Meta:
        model = m.injection
        fields = ['animalID',
            'anatTarget',
            'tracer',
            'injectionMethod',
            'current',
            'seconds_on',
            'seconds_off',
            'nl_per_inject',
            'number_injects',
            'sec_bt_injects',
            'APcoord',
            'LMcoord',
            'DVcoord',
            'beakBarAngle',
            'probeArmAngle',
            'comments']
    def __init__(self,*args, **kwargs):
        super(InjectionForm, self).__init__(*args, **kwargs)
        OPTION_VALUE_1_FIELDS = [
            'nl_per_inject',
            'number_injects',
            'sec_bt_injects']
        OPTION_VALUE_2_FIELDS = [
            'current',
            'seconds_on',
            'seconds_off',
            ]
        for fieldName in OPTION_VALUE_1_FIELDS:            
            self.fields[fieldName].widget.attrs.update({
                'class': 'option_1_fields'
                })
        for fieldName in OPTION_VALUE_2_FIELDS:            
            self.fields[fieldName].widget.attrs.update({
                'class': 'option_2_fields'
                }) 

    def clean(self):
        """
        Custom form validation required to check for unique constraint.
        The meta attribute unique_together won't work here because some fields can be
        null, meaning they will never be equal to each other, and so every model
        instance "appears" unique. To get around this we use a complicated-looking
        QuerySet "get" method that only searches the appropriate fields and also
        ignores the null fields.
        """
        injectMethods = m.injectMethods.objects.all()
        injectMethod_from_Form = self.cleaned_data['injectionMethod'].method
        if injectMethod_from_Form == 'Pressure injection -- Nanoject II':
            try:
                m.injection.objects.get(animalID=self.cleaned_data['animalID'],
                    anatTarget=self.cleaned_data['anatTarget'],
                    tracer=self.cleaned_data['tracer'],
                    nl_per_inject=self.cleaned_data['nl_per_inject'],
                    number_injects=self.cleaned_data['number_injects'],
                    sec_bt_injects=self.cleaned_data['sec_bt_injects'],
                    APcoord=self.cleaned_data['APcoord'],
                    LMcoord=self.cleaned_data['LMcoord'],
                    DVcoord=self.cleaned_data['DVcoord'],
                    beakBarAngle=self.cleaned_data['beakBarAngle'],
                    probeArmAngle=self.cleaned_data['probeArmAngle'])
                raise forms.ValidationError('Injection exists already.')
            except m.injection.MultipleObjectsReturned:
                raise forms.ValidationError('Injection exists already.')
            except m.injection.DoesNotExist:
                pass                
        elif injectMethod_from_Form == 'Iontophoresis': 
            try:
                m.injection.objects.get(animalID=self.cleaned_data['animalID'],
                    anatTarget=self.cleaned_data['anatTarget'],
                    tracer=self.cleaned_data['tracer'],
                    current=self.cleaned_data['current'],
                    seconds_on=self.cleaned_data['seconds_on'],
                    seconds_off=self.cleaned_data['seconds_off'],
                    APcoord=self.cleaned_data['APcoord'],
                    LMcoord=self.cleaned_data['LMcoord'],
                    DVcoord=self.cleaned_data['DVcoord'],
                    beakBarAngle=self.cleaned_data['beakBarAngle'],
                    probeArmAngle=self.cleaned_data['probeArmAngle'])
                raise forms.ValidationError('Injection exists already.')
            except m.injection.MultipleObjectsReturned:
                raise forms.ValidationError('Injection exists already.')            
            except m.injection.DoesNotExist:
                pass                
                
class ResultsForm(forms.ModelForm):
    class Meta:
        model = m.results
        fields = ['animalID',
        'slideNum',
        'sectionNum',
        'result',
        'anatArea',
        'channel']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
                }
            }
        widgets = {
            'slideNum': forms.NumberInput(attrs={'min': 1}),
            'sectionNum': forms.NumberInput(attrs={'min': 1}),
        }
