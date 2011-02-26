from django.contrib import admin
from main.models import Bound

class BoundAdmin(admin.ModelAdmin):
    list_display = ('id', 'min_x', 'min_y', 'max_x', 'max_y')

admin.site.register(Bound, BoundAdmin)

