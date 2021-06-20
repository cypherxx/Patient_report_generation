from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.db.models.base import Model

class CustomUser(AbstractUser):

    contact = models.CharField(max_length=15)

    class Meta:
        ordering = ('-id',)

    def __str__(self):

        return f'{self.first_name}'

class Report_Patient(models.Model):
    patient_id=models.AutoField(primary_key=True)
    ijkname=models.CharField(max_length=100, null=True)
    ijkgender=models.CharField(max_length=100, null=True)
    ijkdot=models.CharField(max_length=100, null=True)
    ijkdob=models.CharField(max_length=100, null=True)
    ijkage=models.IntegerField(null=True)
    ijkinformant=models.CharField(max_length=100, null=True)
    ijkclass=models.CharField(max_length=10,null=True)
    ijk2_age_observation=models.CharField(max_length=100,null=True)
    ijk2_attention=models.CharField(max_length=100,null=True)
    ijkappropriateness=models.CharField(max_length=100,null=True)
    ijkinappropriate=models.CharField(max_length=100,null=True)
    ijkinappropriateness =models.CharField(max_length=100,null=True)
    ijkschonell_list_0=models.CharField(max_length=100,null=True)
    ijkschonell_list_1=models.CharField(max_length=100,null=True)
    ijkschonell_list_2=models.CharField(max_length=100,null=True)
    ijkschonell_list_3=models.CharField(max_length=100,null=True)
    ijkschonell_list_4=models.CharField(max_length=100,null=True)
    ijkschonell_list_5=models.CharField(max_length=100,null=True)
    ijkauditory_res=models.CharField(max_length=100,null=True)
    ijkreport_name=models.CharField(max_length=100,null=True)
    ijk2_referral=models.CharField(max_length=100,null=True)
    ijkschool=models.CharField(max_length=100,null=True)
    ijkcomplaints=models.CharField(max_length=100,null=True)
    ijklanguages=models.CharField(max_length=100,null=True)
    ijk2_qualities=models.CharField(max_length=100,null=True)
    ijk2_response=models.CharField(max_length=100,null=True)
    ijkfinal_review=models.CharField(max_length=100,null=True)
    ijkfinal_percentile=models.CharField(max_length=100,null=True)
    ijkfinal_intelligence=models.CharField(max_length=100,null=True)
    ijkschonell_reading_handwriting=models.CharField(max_length=100,null=True)
    ijkschonell_reading_age=models.CharField(max_length=100,null=True)
    ijkschonell_spelling_age=models.CharField(max_length=100,null=True)
    ijkschonell_summary=models.CharField(max_length=100,null=True)
    ijkschonell_list_7=models.CharField(max_length=100,null=True)
    ijkauditory_age=models.CharField(max_length=100,null=True)
    ijkauditory_summary=models.CharField(max_length=100,null=True)
    ijkauditory_report=models.CharField(max_length=100,null=True)
    ijkfinal_summary=models.CharField(max_length=100,null=True)
    ijktests=models.CharField(max_length=100,null=True)
    ijksattler_table=models.CharField(max_length=100,null=True)
    ijkyear=models.IntegerField(null=True)
    ijkmonth=models.IntegerField(null=True)
    ijkravens_test=models.CharField(max_length=100,null=True)
    ijkverbal_tests_average=models.IntegerField(null=True)
    ijkverbal_tests=models.CharField(max_length=100,null=True)
    ijkfull_score=models.IntegerField(null=True)
    ijkperformance_tests_average=models.IntegerField(null=True)
    ijkperformance_tests=models.CharField(max_length=100,null=True)
    Report = models.FileField(upload_to='media')
    report_name=models.CharField(max_length=100,null=True)
    class Meta:
        ordering = ('-patient_id',)

    def __str__(self):
        return f'{self.ijkname}'




