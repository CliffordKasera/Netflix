from django.contrib import admin

# Register your models here.
# Register your models here.

from .models import User, User_Fav

admin.site.register(User)
admin.site.register(User_Fav)