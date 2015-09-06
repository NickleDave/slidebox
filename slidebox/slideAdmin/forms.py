from django import forms
from django.forms import TextInput
from django.core.exceptions import NON_FIELD_ERRORS

from . import models as m
from .slideAdminUtilityFuncs import convert_to_total_number_of_sections
from .slideAdminUtilityFuncs import convert_to_slide_and_section_number

import pdb

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

    class Meta:
        model = m.injection
        fields = ['animalID',
            'anatTarget',
            'tracer',
            'APcoord',
            'LMcoord',
            'DVcoord',
            'beakBarAngle',
            'probeArmAngle',
            'injectionMethod',
            'current',
            'duration',
            'seconds_on',
            'seconds_off',
            'nl_per_inject',
            'number_injects',
            'sec_bt_injects',
            'time_waited_after_injection',
            'comments']
        widgets = {
            'current': forms.NumberInput(attrs={'min': 0}),
            'duration': forms.NumberInput(attrs={'min': 0}),
            'seconds_on': forms.NumberInput(attrs={'min': 0}),
            'seconds_off': forms.NumberInput(attrs={'min': 0}),
            'nl_per_inject': forms.NumberInput(attrs={'min': 0}),
            'number_injects': forms.NumberInput(attrs={'min': 0}),
            'sec_bt_injects': forms.NumberInput(attrs={'min': 0}),
            'time_waited_after_injection': forms.NumberInput(attrs={'min': 0}),
        }
    def __init__(self,*args, **kwargs):
        super(InjectionForm, self).__init__(*args, **kwargs)
        OPTION_VALUE_1_FIELDS = [
            'nl_per_inject',
            'number_injects',
            'sec_bt_injects']
        OPTION_VALUE_2_FIELDS = [
            'current',
            'duration',
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
        Also need to check that user did not enter values for both pressure injection
        and iontophoresis. If user did, then raise ValidationError saying to
        choose only one method."
        """
        super(InjectionForm, self).clean()
        # validate uniqueness
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
                    duration=self.cleaned_data['duration'],
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
        #check if user entered something in fields not associated with the chosen injection method
#        if self.cleaned_data['injectionMethod'].method == 'Pressure injection -- Nanoject II' \
#            and (self.cleaned_data['current'] is not None or \
#                 self.cleaned_data['seconds_on'] is not None or \
#                 self.cleaned_data['seconds_off'] is not None or \
#                 self.cleaned_data['duration'] is not None):
#            raise forms.ValidationError(
#                'Values entered in iontophoresis fields but method is pressure injection')
#        if self.cleaned_data['injectionMethod'].method == 'Iontophoresis' \
#            and (self.cleaned_data['nl_per_inject'] is not None or \
#                 self.cleaned_data['number_injects'] is not None or \
#                 self.cleaned_data['sec_bt_injects'] is not None):
#            raise forms.ValidationError(
#                'Values entered in pressure injection fields but method is iontophoresis')
        
class ResultsForm(forms.ModelForm):
    extend_same_result = forms.BooleanField(
        label='Extend same result from slide and section above to another slide and section',
        required=False)
    slide_number_to_extend_to = forms.IntegerField(min_value=1,
        required=False,
        widget=forms.NumberInput(attrs={
            'class':'extend_result_fields'})
            )
    section_number_to_extend_to = forms.IntegerField(min_value=1,
            required=False,
            widget=forms.NumberInput(attrs={
            'class':'extend_result_fields'})
            )

    def clean(self):
        cleaned_data = super(ResultsForm, self).clean()
        if cleaned_data['extend_same_result']:
            start_slideNum = cleaned_data['slideNum']
            start_sectionNum = cleaned_data['sectionNum']
            end_slideNum = cleaned_data['slide_number_to_extend_to']
            end_sectionNum = cleaned_data['section_number_to_extend_to']
            if start_slideNum==end_slideNum and start_sectionNum==end_sectionNum:
                raise forms.ValidationError(
                    'Can\'t extend result to same slide and section number')
            else:
                sections_per_slide = cleaned_data['animalID'].sectionsPerSlide
                if end_slideNum > start_slideNum or \
                    (end_slideNum==start_slideNum and end_sectionNum > start_sectionNum):
                    count_up = True
                    if start_sectionNum >= sections_per_slide:
                        curr_sectionNum = 1
                        curr_slideNum = start_slideNum + 1
                    else:
                        curr_sectionNum = start_sectionNum + 1
                        curr_slideNum = start_slideNum
                elif end_slideNum < start_slideNum or \
                    (end_slideNum==start_slideNum and end_sectionNum < start_sectionNum):
                    count_down = True
                    if start_sectionNum == 1:
                        curr_sectionNum = sections_per_slide
                        curr_slideNum = start_slideNum - 1
                    else:
                        curr_sectionNum = start_sectionNum - 1
                        curr_slideNum = start_slideNum
            pdb.set_trace()
            while True:
                m.results.objects.create(
                    slideNum = curr_slideNum,
                    sectionNum  = curr_sectionNum,
                    animalID = cleaned_data['animalID'],
                    anatArea = cleaned_data['anatArea'],
                    result = cleaned_data['result'],
                    channel =cleaned_data['channel'], 
                    )
                if curr_sectionNum == end_sectionNum and curr_slideNum  == end_slideNum:
                    break
                if count_up:
                    if curr_sectionNum >= sections_per_slide:
                            curr_sectionNum = 1
                            curr_slideNum += 1
                    else:
                            curr_sectionNum += 1
                elif count_down:
                    if curr_sectionNum == 1:
                        curr_sectionNum = sections_per_slide
                        curr_slideNum -= 1
                    else:
                        curr_sectionNum -= 1

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

class search_animal_form(forms.Form):
    ID_errs = {'invalid':'Animal ID must consist of two sets of two letters and 1-3 numbers, e.g., gy6or113'}
    animal_ID = forms.RegexField(label="animal ID",
        regex='[a-z]{2}[0-9]{1,3}[a-z]{2}[0-9]{1,3}',
        max_length=10,
        error_messages=ID_errs)

class search_inject_form(forms.Form):
    anat_target = forms.ModelChoiceField(queryset=m.anatAreas.objects.all(),label='anatomical target')
    tracer_type = forms.ModelChoiceField(queryset=m.tracerTypes.objects.all())
    surgery_date_after = forms.DateField()
    surgery_date_before = forms.DateField()
            
class find_distance_form(forms.Form):
    # can only estimate distance from midline by counting sections
    # if the brain was cut parasagitally; so, filter animalIDs to return only
    # those cut parasagitally
    animalIDs = forms.ModelMultipleChoiceField(
        label = 'animal ID (selecting multiple returns average)',
        queryset = m.animalID.objects.filter(sectionPlane='PS'))
    anatAreas = forms.ModelChoiceField(
        label = 'anatomical area',
        queryset = m.anatAreas.objects.all(),
        empty_label=None)
    resultType = forms.ModelChoiceField(
        label = 'result type',
        queryset = m.resultTypes.objects.all(),
        empty_label=None)

    def clean(self):
        cleaned_data = super(find_distance_form, self).clean()
        #first make sure that anatomical area that user is searching for has been
        #entered as a result in the animalID(s) user is searching
        anatArea_pk = cleaned_data['anatAreas'].pk
        #MultipleModelChoice field returns a list, have to access with index
        for curr_animalID in cleaned_data['animalIDs']:
            if not m.results.objects.filter(animalID=curr_animalID,anatArea=anatArea_pk).exists():
                raise forms.ValidationError('Selected anatomical area not found in selected animals')
            #Problem: if there are multiple sections with the area entered in the form, it will blow up
            #the measure function below (when the function tries to "get" the appropriate slide and section
            #number with a QuerySet and multiple objects are returned, this will raise an error)
        
    def measure(self):
        cleaned_data = self.cleaned_data
        animalIDs = cleaned_data['animalIDs']
        anatArea_pk = cleaned_data['anatAreas'].pk
        InC_pk = m.anatAreas.objects.get(abbreviation='InC').pk
        sections_with_InC = \
            m.results.objects.filter(animalID=animalIDs,anatArea=InC_pk).values('slideNum','sectionNum')
        for curr_animalID in animalIDs:
            curr_anatArea = m.results.objects.get(animalID=curr_animalID,
                anatArea=anatArea_pk)
            curr_anatArea_section = convert_to_total_number_of_sections(
                    curr_animalID,
                    curr_anatArea.slideNum,
                    curr_anatArea.sectionNum)
            InC_sections = []
            for InC_results in m.results.objects.filter(animalID=curr_animalID,anatArea=InC_pk):
                InC_sections.append(convert_to_total_number_of_sections(
                    curr_animalID,
                    InC_results.slideNum,
                    InC_results.sectionNum))
            takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
            InC_section_to_use = takeClosest(curr_anatArea_section,InC_sections)
            distance = (curr_anatArea_section - InC_section_to_use + 1) * curr_animalID.sectionThickness
            cleaned_data['distance'] = distance
        return cleaned_data
