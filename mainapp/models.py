from django.db import models

# Create your models here.
class Job(models.Model):
    job_title=models.CharField( blank=True, max_length=1000)
    company_name=models.CharField( blank=True, max_length=1000)
    location=models.CharField( blank=True, max_length=1000)
    job_nature=models.CharField( blank=True, max_length=1000)
    job_pay=models.CharField( blank=True, max_length=1000)
    joy_currency=models.CharField( blank=True, max_length=1000)
    posted=models.CharField( blank=True, max_length=1000)
    job_summary=models.CharField( blank=True, max_length=1000)
    read_more=models.CharField( blank=True, max_length=1000)
