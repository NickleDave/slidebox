from django.contrib import admin

from slideAdmin.models import animalID
from slideAdmin.models import anatAreas
from slideAdmin.models import tracers
from slideAdmin.models import solvents
from slideAdmin.models import tracerTypes
from slideAdmin.models import injectMethods
from slideAdmin.models import injection
from slideAdmin.models import resultTypes
from slideAdmin.models import channelTypes
from slideAdmin.models import results

# Register your models here.
admin.site.register(animalID)
admin.site.register(anatAreas)
admin.site.register(tracers)
admin.site.register(solvents)
admin.site.register(tracerTypes)
admin.site.register(injectMethods)
admin.site.register(injection)
admin.site.register(resultTypes)
admin.site.register(channelTypes)
admin.site.register(results)


