from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Eleman
from .models import Kelime


class ElemanInline(admin.StackedInline):
    model = Eleman
    can_delete = False
    verbose_name_plural = 'eleman'


class UserAdmin(BaseUserAdmin):
    inlines = (ElemanInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Kelime)
