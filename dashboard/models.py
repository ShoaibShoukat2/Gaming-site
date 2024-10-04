from django.db import models
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField


class OrganizationSetting(models.Model):
    site_title = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='CompanyLogo/', verbose_name='Select Logo')
    favicon = models.ImageField(upload_to='Favicon/', verbose_name='Select favicon')
    meta_name = models.CharField(max_length=200)
    meta_description = models.TextField()
    meta_property = models.TextField()
    description = models.TextField()
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return self.site_title

class TermsAndCondition(models.Model):
    terms = RichTextField()

class HelpCenter(models.Model):
    help_center = RichTextField()



