from . models import *

def organization_info(request):
    organization_info= OrganizationSetting.objects.first()
    return{
        'organization_info':organization_info
    }




