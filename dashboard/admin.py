from django.contrib import admin
from .models import *

# Register your models here.

class OrganizationSettingAdmin(admin.ModelAdmin):
    model= OrganizationSetting
    list_display =['site_title','logo','favicon','meta_name','meta_description', 'meta_property', 'keyword', 'description']    
admin.site.register(OrganizationSetting, OrganizationSettingAdmin)

admin.site.register(TermsAndCondition)
admin.site.register(HelpCenter)

