from django.contrib import admin

from awwardsapp.models import Profile,Project,Rating

admin.site.register(Profile)
admin.site.register(Rating)
admin.site.register(Project)
