from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class animalID(models.Model):
    IDnumber = models.CharField(verbose_name='animal ID',max_length = 10,
        validators=[RegexValidator(regex=r'[a-z]{2}[0-9]{2,3}',
            message="Animal ID must consist of two sets of two letters and 1-3 numbers, e.g., gy6or113")])
    surgeryDate = models.DateField('date of surgery')
    perfusionDate = models.DateField('date of perfusion')
    surgeryNotebook = models.IntegerField('surgery notebook',validators=[MinValueValidator(1)])
    surgeryNotebookPage = models.IntegerField('surgery notebook page',validators=[MinValueValidator(1)])
    sectionDate = models.DateField('sectioning data')
    sectionsPerSlide = models.IntegerField('sections per slide',default=6,
        validators=[MinValueValidator(1)]
        )

    PARASAGITTAL = 'PS'
    CORONAL = 'CO'
    HORIZONTAL = 'HO'
    SECTION_PLANE_CHOICES = ((PARASAGITTAL, 'Parasagittal'),
		(CORONAL, 'Coronal'),
		(HORIZONTAL, 'Horizontal'),
	)

    sectionPlane = models.CharField('plane of section',max_length = 2,choices = SECTION_PLANE_CHOICES,
	default = PARASAGITTAL)

    sectionThickness = models.IntegerField('section thickness',validators=[MinValueValidator(1)])

    def clean(self):
        if self.perfusionDate < self.surgeryDate:
            raise ValidationError('date of perfusion cannot be before date of surgery')
        if self.sectionDate < self.perfusionDate:
            raise ValidationError('date of sectioning cannot be before date of perfusion')
    
    def __str__(self):
        return self.IDnumber

#models referenced by injection
class anatAreas(models.Model):
    areaName = models.CharField('anatomical area name',max_length = 100)
    abbreviation = models.CharField(max_length = 5)
    def __str__(self):
        return self.areaName

    class Meta:
        verbose_name = 'anatomical area'
		
class tracers(models.Model):
	nameOfTracer = models.CharField(max_length=50)
	def __str__(self):
		return self.nameOfTracer

	class Meta:
		verbose_name = 'tracer'

class solvents(models.Model):
	nameOfSolvent = models.CharField(max_length=50)
	def __str__(self):
		return self.nameOfSolvent

	class Meta:
		verbose_name = 'solvent'

		
class tracerTypes(models.Model):
	percentDilution = models.DecimalField(max_digits = 5,decimal_places = 2)
	tracerName = models.ForeignKey(tracers)
	solventName = models.ForeignKey(solvents)
	def __str__(self):
		return '%d%% %s in %s' % (self.percentDilution,self.tracerName,self.solventName)
		
	class Meta:
		verbose_name = 'tracer, percent solution, and solvent'

class injectMethods(models.Model):
    method = models.CharField('injection method',max_length = 100)
    def __str__(self):
        return self.method

class injection(models.Model):
    animalID = models.ForeignKey(animalID,default=None,verbose_name="animal ID")
    anatTarget = models.ForeignKey(anatAreas,verbose_name="anatomical target")
    tracer = models.ForeignKey(tracerTypes)
    injectionMethod = models.ForeignKey(injectMethods,verbose_name="injection method")
    current = models.IntegerField('current in uA',validators=[MinValueValidator(0)],null=True,blank=True)
    seconds_on = models.DecimalField('seconds on',
        validators=[MinValueValidator(0)],
        null=True,blank=True,
        max_digits = 3,decimal_places=1)
    seconds_off = models.DecimalField('seconds off',
        validators=[MinValueValidator(0)],
        null=True,blank=True,
        max_digits = 3,decimal_places=1)
    duration = models.IntegerField('duration (minutes)',validators=[MinValueValidator(0)],null=True,blank=True)
    nl_per_inject = models.DecimalField('nanoliters per inject',
        validators=[MinValueValidator(0)],
        null=True,blank=True,
        max_digits = 3,decimal_places=1)
    number_injects = models.IntegerField('number of times "Inject" was pressed',
        validators=[MinValueValidator(0)],null=True,blank=True)
    sec_bt_injects = models.IntegerField('seconds waited between pressing "Inject"',
        validators=[MinValueValidator(0)],null=True,blank=True)
    APcoord = models.DecimalField('anterior-posterior co-ordinate',
        max_digits=3,decimal_places=2)
    LMcoord = models.DecimalField('lateral-medial co-ordinate',
        max_digits=3,decimal_places=2)
    DVcoord = models.DecimalField('dorsal-ventral co-ordinate',
        max_digits=3,decimal_places=2)
    time_waited_after_injection = models.IntegerField('Time waited after injection (minutes)',
        validators=[MinValueValidator(0)],null=True,blank=True)
    beakBarAngle = models.DecimalField('beak bar angle', max_digits = 3,decimal_places=1)
    probeArmAngle = models.DecimalField('probe arm angle',max_digits = 3,decimal_places=1)
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return '%s, %s; AP co-ord:%4.2f LM co-ord:%4.2f DV co-ord:%4.2f' % (self.animalID,
        self.anatTarget,
        self.APcoord,
        self.LMcoord,
        self.DVcoord)
            
class resultTypes(models.Model):
    result = models.CharField('result type',max_length=50)
    def __str__(self):
        return self.result

class channelTypes(models.Model):
    channel = models.CharField('channel name',max_length=50)
    def __str__(self):
        return self.channel
    
class results(models.Model):
    animalID = models.ForeignKey(animalID)
    slideNum  = models.IntegerField('slide number',validators=[MinValueValidator(1)])
    sectionNum = models.IntegerField('section number',validators=[MinValueValidator(1)])
    result = models.ForeignKey(resultTypes)
    anatArea = models.ForeignKey(anatAreas)
    channel = models.ForeignKey(channelTypes)
    def __str__(self):
        return '%s, slide %d, section %d: %s in %s -- %s channel' % (self.animalID,
        self.slideNum,
        self.sectionNum,
        self.result,
        self.anatArea,
        self.channel)
    class Meta:
        unique_together = (("animalID","slideNum", "sectionNum", "result", "anatArea", "channel"),)
