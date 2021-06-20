from django.db.models.expressions import RawSQL
from django.http import response
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import CustomUser, Report_Patient
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
import hashlib
from easy_pdf.rendering import render_to_pdf_response,render_to_pdf
import os, json
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import mimetypes


# Define function to download pdf file using template

global hash_util
hash_util = os.environ.get('verification_hash') or 'random_string'

def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        f_name=request.POST.get('first_name')
        l_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('mobile')
        password=request.POST.get('password')
        print(username,f_name,l_name,email,password,phone)
        new_user=CustomUser.objects.create_user(username=username, first_name=f_name, last_name=l_name, password=password,email=email, contact=phone)
        new_user.is_active=False
        new_user.save()
        global hash_util
        hash_object = hashlib.md5((email + hash_util).encode())
        hashed_string = hash_object.hexdigest()
        subject, from_email, to = 'Verification', settings.EMAIL_HOST_USER, email
        url = f"{request.scheme}://{request.get_host()}{reverse('verify')}?key={hashed_string}&email={email}"
        html_content = render_to_string('html/verification_template.html', {'url': url})      
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        return render(request, 'html/sign-in.html')
    else:
        return render(request, 'html/register.html')

@login_required(login_url='sign_in')
def user_profile(request):
    return render(request,'html/user_profile.html')

@login_required(login_url='sign_in')
def send_report_mail(request,pk):

    x = Report_Patient.objects.get(pk=pk)
    print(x)
    return render(request,'html/send_mail.html',{'x':x})

@login_required(login_url='sign_in')
def report_mail(request,pk):

    x = Report_Patient.objects.get(pk=pk)
    email_id = request.POST['email']
    mail = EmailMessage('Report','Attached Report with this mail',settings.EMAIL_HOST_USER,[email_id])
    r = x.report
    mail.attach(r.name,r.read())
    mail.send()
    return redirect('index')


def verify(request):
    global hash_util
    email = request.GET['email']
    key = request.GET['key']

    if hashlib.md5((email + hash_util).encode()).hexdigest() == key:
        messages.success(request, 'Verification successful', 'success')
        user = CustomUser.objects.get(email=email)
        user.is_active = True
        user.save()
        return redirect(reverse('sign_in'))
    messages.error(request, 'Verification failed', 'error')
    return redirect('/')


@login_required(login_url='sign_in')
def index(request):
    patient = list(Report_Patient.objects.values())
    print(patient)
    l=[]
    for i in patient:
        x = list(i.values())
        l.append(x)
    print(patient)
    Url = f"{request.scheme}://{request.get_host()}/media/"
    return render(request, 'html/index.html',{'p':l,'u':Url})

def sign_in(request):
    if request.method == 'GET':
        return render(request, 'html/sign-in.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(reverse('index'))
        return HttpResponse('<h1>Sorry, no such user</h1>')

@login_required(login_url='sign_in')
def sign_out(request):
    if request.user.is_anonymous:
        return redirect(reverse('index'))
    logout(request)
    return redirect(reverse('sign_in'))


class new_profile(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'report/report.html')


class get_report(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    global data
    def get(self, request):
        global data
        return render_to_pdf_response(request,'html/generate_pdf.html',data,filename='report-.pdf')
    def post(self, request):
        global data
        
        data = json.loads(request.body)
        k=['name', 'gender', 'dot', 'dob', 'age', 'informant', 'class', '2_age_observation', '2_attention', 'appropriateness', 'inappropriate ', 'inappropriateness ', 'schonell_list_0', 'schonell_list_1', 'schonell_list_2', 'schonell_list_3', 'schonell_list_4', 'schonell_list_5', 'auditory_res', 'csrfmiddlewaretoken', '', '2_referral', 'school', 'complaints', 'languages', '2_qualities', '2_response', 'final_review', 'final_percentile', 'final_intelligence', 'schonell_reading_handwriting', 'schonell_reading_age', 'schonell_spelling_age', 'schonell_summary', 'schonell_list_7', 'auditory_age', 'auditory_summary', 'auditory_report', 'final_summary', 'tests', 'sattler_table', 'year', 'month', 'ravens_test', 'verbal_tests_average', 'verbal_tests', 'full_score', 'performance_tests_average', 'performance_tests']
        a=list(data.keys())
        for i in k:
            if i not in a:
                data[i]=None
        per = data.get('performance_tests')
        ver  =data.get('verbal_tests')
        if not per:
            data['performance_tests'] = [0,0,0,0,0]
        if not ver:
            data['verbal_tests'] = [0,0,0,0,0]
        new_object=Report_Patient.objects.create(ijkname=data['name'],
                                            ijkgender=data['gender'],
                                            ijkdot=data['dot'],
                                            ijkdob=data['dob'],
                                            ijkage=data['age'],
                                            ijkinformant=data['informant'],
                                            ijkclass=data['class'],
                                            ijk2_age_observation=data['2_age_observation'],
                                            ijk2_attention=data['2_attention'],
                                            ijkappropriateness=data['appropriateness'],
                                            ijkinappropriate =data['inappropriate '],
                                            ijkinappropriateness =data['inappropriateness '],
                                            ijkschonell_list_0=data['schonell_list_0'],
                                            ijkschonell_list_1=data['schonell_list_1'],
                                            ijkschonell_list_2=data['schonell_list_2'],
                                            ijkschonell_list_3=data['schonell_list_3'],
                                            ijkschonell_list_4=data['schonell_list_4'],
                                            ijkschonell_list_5=data['schonell_list_5'],
                                            ijkauditory_res=data['auditory_res'],
                                            ijk2_referral=data['2_referral'],
                                            ijkschool=data['school'],
                                            ijkcomplaints=data['complaints'],
                                            ijklanguages=data['languages'],
                                            ijk2_qualities=data['2_qualities'],
                                            ijk2_response=data['2_response'],
                                            ijkfinal_review=data['final_review'],
                                            ijkfinal_percentile=data['final_percentile'],
                                            ijkfinal_intelligence=data['final_intelligence'],
                                            ijkschonell_reading_handwriting=data['schonell_reading_handwriting'],
                                            ijkschonell_reading_age=data['schonell_reading_age'],
                                            ijkschonell_spelling_age=data['schonell_spelling_age'],
                                            ijkschonell_summary=data['schonell_summary'],
                                            ijkschonell_list_7=data['schonell_list_7'],
                                            ijkauditory_age=data['auditory_age'],
                                            ijkauditory_summary=data['auditory_summary'],
                                            ijkauditory_report=data['auditory_report'],
                                            ijkfinal_summary=data['final_summary'],
                                            ijktests=data['tests'],
                                            ijksattler_table=data['sattler_table'],
                                            ijkyear=data['year'],
                                            ijkmonth=data['month'],
                                            ijkravens_test=data['ravens_test'],
                                            ijkverbal_tests_average=data['verbal_tests_average'],
                                            ijkverbal_tests=data['verbal_tests'],
                                            ijkfull_score=data['full_score'],
                                            ijkperformance_tests_average=data['performance_tests_average'],
                                            ijkperformance_tests=data['performance_tests'])
        new_object.save()
        # for i in keys:
        #     z=Report_Patient.objects.order_by('-patient_id')[0]
        #     y=x+i
        #     print(y)
        #     if type(data[i])==type(keys):
        #         xx=json.dumps(data[i])
        #         z.y=xx
        #     else:
        #         z.y=data[i]
        # z.save()
        return JsonResponse({'status':201,"msg":"Working Correctly"})
    
@login_required(login_url='sign_in')
def detail(request):
    x=Report_Patient.objects.order_by('-patient_id')[0]
    print(x)
    pdf = request.FILES['Report']
    print(pdf)
    x.Report=pdf
    x.save()
    return redirect('index')

def edit(request):
    return HttpResponse("Pass")
    

