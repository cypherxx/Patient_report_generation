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
        #print(username,f_name,l_name,email,password,phone)
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
    #print(x)
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
    #print(patient)
    l=[]
    for i in patient:
        x = list(i.values())
        l.append(x)
    #print(patient)
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
        ver = data.get('verbal_tests')
        if not per:
            data['performance_tests'] = [0,0,0,0,0]
        if not ver:
            data['verbal_tests'] = [0,0,0,0,0]
        
        if(data['update_record']!='0'):
            #print(data)
            x=data['update_record']
            #print(x)
            new_object=Report_Patient.objects.get(patient_id=int(x))
            print(new_object.ijkname)
            new_object.ijkname=data['name']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkgender=data['gender']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkdot=data['dot']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkdob=data['dob']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkinformant=data['informant']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkclass=data['class']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijk2_age_observation=data['2_age_observation']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijk2_attention=data['2_attention']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkappropriateness=data['appropriateness']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkinappropriate =data['inappropriate ']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkinappropriateness =data['inappropriateness ']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_list_0=data['schonell_list_0']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_list_1=data['schonell_list_1']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_list_2=data['schonell_list_2']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_list_3=data['schonell_list_3']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_list_4=data['schonell_list_4']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_list_5=data['schonell_list_5']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkauditory_res=data['auditory_res']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijk2_referral=data['2_referral']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschool=data['school']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkcomplaints=data['complaints']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijklanguages=data['languages']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijk2_qualities=data['2_qualities']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijk2_response=data['2_response']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkfinal_review=data['final_review']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkfinal_percentile=data['final_percentile']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkfinal_intelligence=data['final_intelligence']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_reading_handwriting=data['schonell_reading_handwriting']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_reading_age=data['schonell_reading_age']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_spelling_age=data['schonell_spelling_age']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_summary=data['schonell_summary']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkschonell_list_7=data['schonell_list_7']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkauditory_age=data['auditory_age']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkauditory_summary=data['auditory_summary']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkauditory_report=data['auditory_report']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkfinal_summary=data['final_summary']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijktests=data['tests']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijksattler_table=data['sattler_table']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkyear=data['year']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkmonth=data['month']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkravens_test=data['ravens_test']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkverbal_tests_average=data['verbal_tests_average']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkverbal_tests=data['verbal_tests']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkfull_score=data['full_score']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkperformance_tests_average=data['performance_tests_average']
            new_object.save()
            new_object=Report_Patient.objects.get(patient_id=int(x))
            new_object.ijkperformance_tests=data['performance_tests']
            new_object.save()
            
        else:
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
        return JsonResponse({'status':201,"msg":"Working Correctly"})
    
@login_required(login_url='sign_in')
def detail(request):
    x=Report_Patient.objects.order_by('-patient_id')[0]
    #print(x)
    pdf = request.FILES['Report']
    #print(pdf)
    x.Report=pdf
    x.save()
    return redirect('index')
@login_required(login_url='sign_in')
def update_detail(request):
    x=Report_Patient.objects.get(patient_id=request.POST.get('report_id'))
    #print(x)
    pdf = request.FILES['Report']
    #print(pdf)
    x.Report=pdf
    x.save()
    return redirect('index')
def edit(request):
    p_id=request.POST.get("edit")
    x=p_id[5:]
    my_obj=Report_Patient.objects.filter(patient_id=x)
    y= (list(my_obj.values()))
    obj_keys= list(y[0].keys())
    obj_values= list(y[0].values())
    flag=0
    for i in range(0,len(obj_values)):
        item=obj_values[i]
        if type(item)==type("str"):
            if item[0]=='[':
                st='obj_values[i]='
                exec(st+item)
                flag+=1
                if(flag==1):
                    for j in range(0,len(obj_values[i])):
                        if obj_values[i][j]==True:
                            obj_values[i][j]='checked'
                        else:
                            obj_values[i][j]=''
                    print(obj_values[i])
                elif(flag==2):
                    print(obj_values[i])
                    for j in range(0,len(obj_values[i])):
                        for k in range(0,5):
                            if obj_values[i][j][k]==True:
                                obj_values[i][j][k]='checked'
                            else:
                                obj_values[i][j][k]=''
                    print(obj_values[i])                   

    return render(request, 'report/report_edit.html', {'key':obj_keys, 'value': obj_values})
    

