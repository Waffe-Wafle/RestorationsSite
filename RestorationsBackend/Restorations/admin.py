from django.contrib import admin
from .models import *

admin.site.register([
    RestoreWork, Donater, Donation, RestorationRestore
])