
from django.contrib import admin
from .models import CustomUser,Report_Patient
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display=['first_name','last_name','email','contact']
    add_fieldsets= BaseUserAdmin.add_fieldsets+(
        (None,{'fields':('first_name','last_name','email','contact')}),
    )
    fieldsets = BaseUserAdmin.fieldsets+(
        (None,{'fields':('contact',)}),
    )
admin.site.register(CustomUser,CustomUserAdmin)

admin.site.register(Report_Patient)