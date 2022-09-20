# from asyncio.events import _Context
from linecache import lazycache
from multiprocessing import context
from multiprocessing.dummy import current_process
from unicodedata import name
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from requests import request
from .models import Test,shopping_cart,product,purchase_record_model
from django.urls import reverse
from django.template import loader
# from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm,User_form
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.messages import get_messages
from datetime import datetime, timedelta


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return str(obj)
        return super().default(obj)
# from django.db.models.query_utils import Q
# def index(request):
#   template = loader.get_template('first.html')
#   return HttpResponse(template.render())

# Create your views here.
def index(request):
  search= request.POST.get('search') if request.POST.get('search') else ''
  gender=request.POST.getlist('gender') if request.POST.getlist('gender') else ['girl','boy']
  class_members=Test.objects.filter(name__contains=search,gender__in=gender).values()
  pd=product.objects.all()
  limit=5
  paginator=Paginator(class_members,limit)
  page=request.GET.get('page')
  try:
    class_members=paginator.page(page)
  except PageNotAnInteger:
    class_members=paginator.page(1)
  except EmptyPage:
    class_members=paginator.page(paginator.num_pages)
  try:
    user=User.objects.get(id=request.user.id)
    products=user.usernameOf.all()
    count=products.count()
  except User.DoesNotExist:
    count=0
  context={
    'class_members':class_members,
    'gender':gender,
    'search_name':search,
    'user':request.user,
    'shopping_cart_count':count,
    'pd':pd
  }
  return render(request,"first.html",context)
# @login_required(login_url='/login')
def add(request):
  return render(request,"add.html",{})

def add_record(request):
  y = request.POST['name']
  z = request.POST['gender']
  member = Test( name=y,gender=z)
  member.save()  
  return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/model/login/')
def delete(request,id):
  if str(request.user) != 'admin':
    return HttpResponse('你沒有權限')
  member=Test.objects.get(id=id)
  member.delete()
  return HttpResponseRedirect(reverse('index'))
  
def test1(request):
  limit=5
  test=Test.objects.all()
  paginator=Paginator(test,limit)
  
  page=request.GET.get('page')
  try:
    test=paginator.page(page)
  except PageNotAnInteger:
    test=paginator.page(1)
  except EmptyPage:
    test=paginator.page(paginator.num_pages)
  context={
    'test':test
  }
  return render(request,"test1.html",context)
def login_page(request):
  page='login'
  if request.user.is_authenticated:
    return redirect('index')
  if request.method=='POST':
    username=request.POST.get('username')
    password=request.POST.get('password')
    # try:
    #   user=User.objects.get(username=username)
    # except:
    #   messages.error(request,'用戶不存在')
    user=authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect('index')
    else:
      messages.error(request,'用戶或密碼錯誤')
  context={
    'page':page
  }
  return render(request,'login_.html',context)
def logoutUser(request):
  logout(request)
  return redirect('home')

def register_User(request):
  form=RegisterForm()
  if request.method == 'POST':
    form=RegisterForm(request.POST)
    if form.is_valid():
      user=form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request,user)
      return redirect('index')
  context={
    'form':form,

  }
  return render(request,'login1.html',context)

def update_user(request):
  
  context={

  }
  return render(request,'profile.html',context)
@login_required(login_url='/model/login/')
def profile(request,pk):
  user=request.user
  firstname= request.POST.get('new_first_name') if request.POST.get('new_first_name') else request.POST.get('first_name') if request.POST.get('first_name') else user.first_name
  lastname= request.POST.get('new_last_name') if request.POST.get('new_last_name') else request.POST.get('last_name') if request.POST.get('last_name') else user.last_name
  email=request.POST.get('new_email') if request.POST.get('new_email') else request.POST.get('email') if request.POST.get('email') else user.email
  
  form=User_form(instance=user)
  if request.POST.get('confirm')=='更改':
    if request.method == 'POST':
      form=User_form(request.POST,instance=user)
      if form.is_valid():
          form.save()
          return redirect('index')
  context={
    'first_name':firstname,
    'last_name':lastname,
    'email':email,
    'form':form,
    'str':['id_username','id_email']
  }
  return render(request,'profile.html',context)


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email,'cbf108022@stmail.nptu.edu.tw' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('發生錯誤')
					return redirect ("password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})
@login_required(login_url='/model/login/')
def add_product(request):
  pk=request.POST.get('pk')
  try:
    product_=shopping_cart.objects.get(username=User.objects.get(id=request.user.id),product_name=product.objects.get(id=pk))
    # print(product_.counts)
    product_.counts+=1
    product_.save()
  except shopping_cart.DoesNotExist:
    product_=shopping_cart(username=User.objects.get(id=request.user.id),
                        product_name=product.objects.get(id=pk)
                        )
    product_.save()
  try:
    user=User.objects.get(id=request.user.id)
    products=user.usernameOf.all()
    count=products.count()
  except User.DoesNotExist:
    count=0
  storage = get_messages(request)
  for message in storage:
    print(message)
  return JsonResponse({'count':count})
@login_required(login_url='/model/login1/')
@csrf_exempt
def shopping_carts(request):
  user=User.objects.get(id=request.user.id)
  products=user.usernameOf.all()
  # if request.method=='POST':
  if is_ajax(request=request):
    # print(request.POST.get('id'),request.POST.get('select_value'))
    product=user.usernameOf.filter(product_name=request.POST.get('id'))
    a=1
    text_id='text_'+request.POST.get('id')
    if request.POST.get('input_value')=='+':
      a=int(request.POST.get('data'))+1
    if request.POST.get('input_value')=='-':
      a=int(request.POST.get('data'))-1
    if request.POST.get('input_value')=='text':
      a=int(request.POST.get('data'))   
    for i in product:
      i.counts=a
      i.save()
    return JsonResponse({'test':a,'id':text_id})
  context={
    'products':products,
    'count':products.count(),
    'range':range(1,11)
  }
  return render(request,'shopping_cart.html',context)
@login_required(login_url='/model/login/')
def delete_product(request,pk):
  product=shopping_cart.objects.get(id=pk)
  product.delete()
  return HttpResponseRedirect(reverse('shopping_cart'))
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
@csrf_exempt
def add_product2(request):
  a=1
  text_id='text_'+request.POST.get('id')
  if request.POST.get('input_value')=='+':
    a=int(request.POST.get('data'))+1
  if request.POST.get('input_value')=='-':
    a=int(request.POST.get('data'))-1
  if request.POST.get('input_value')=='text':
    a=int(request.POST.get('data'))
  print(text_id)
  # a=int(request.POST.get('input_value'))+int(request.POST.get('data'))
  # if request.POST.get('id')=='text':
  #   a=request.POST.get('input_value')
  #   print(a)
  return JsonResponse({'test':a,'id':text_id})
def home(request):
  ce=product.objects.values('category').distinct()
  try:
    user=User.objects.get(id=request.user.id)
    products=user.usernameOf.all()
    count=products.count()
  except User.DoesNotExist:
    count=0
  context={
    'shopping_cart_count':count,
    'first_ce':ce[0],
    'category':ce[1:],
  }
  return render(request,'home.html',context)
def login1(request):
  page='login'
  if request.user.is_authenticated:
    return redirect('home')
  if request.method=='POST':
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect('home')
    else:
      messages.error(request,'用戶或密碼錯誤')
  context={
    'page':page
  }
  return render(request,'login1.html',context)
def member_center(request):
  
  context={

  }
  return render(request,'member_centre.html',context)
def member_profile(request):
  user=request.user
  firstname= request.POST.get('new_first_name') if request.POST.get('new_first_name') else request.POST.get('first_name') if request.POST.get('first_name') else user.first_name
  lastname= request.POST.get('new_last_name') if request.POST.get('new_last_name') else request.POST.get('last_name') if request.POST.get('last_name') else user.last_name
  email=request.POST.get('new_email') if request.POST.get('new_email') else request.POST.get('email') if request.POST.get('email') else user.email
  
  form=User_form(instance=user)
  if request.POST.get('confirm')=='更改':
    if request.method == 'POST':
      form=User_form(request.POST,instance=user)
      if form.is_valid():
          form.save()
          return redirect('home')
  context={
    'first_name':firstname,
    'last_name':lastname,
    'email':email,
    'form':form,
    'str':['id_username','id_email']
  }
  return render(request,'member_profile.html',context)
def product_page(request,pk):
  pd=product.objects.get(id=pk)
  f=pd.product_name
  f=f.replace(' ','_')
  context={
    'pd_name':'images/'+f+'.png',
    'pd':pd,
    'details':pd.Details
  }
  return render(request,'product.html',context)
def buy(request):
  user=User.objects.get(id=request.user.id)
  products=user.usernameOf.all()
  all_product=product.objects.all()
  sum_price=0
  for i in all_product:
    for l in products:
      if i.id==l.product_name.id:
        sum_price+=l.counts*i.price
        i.number_of_purchases+=1
        i.save()
  for i in products:
    pr=purchase_record_model(username=i.username,product_name=i.product_name)
    pr.save()
  subject = "購買成功"
  c={
    'pd':products,
    'total':sum_price
  }
  email_template_name="buy.html"
  email=render_to_string(email_template_name,c)
  send_mail(subject, email,'cbf108022@stmail.nptu.edu.tw' , [user.email], fail_silently=False,html_message=email)
  products.delete()
  return render(request,'shopping_cart.html',{})
def category(request,pk):
  ce=product.objects.values('category').distinct()
  pd=product.objects.filter(category=pk)
  try:
    user=User.objects.get(id=request.user.id)
    products=user.usernameOf.all()
    count=products.count()
  except User.DoesNotExist:
    count=0
  context={
    'shopping_cart_count':count,
    'pd':pd,
    'pk':pk,
    'first_ce':ce[0],
    'category':ce[1:],
  }
  return render(request,'category.html',context)
def purchase_record(request):
  # 取得購買清單
  startdate = datetime.today()
  enddate = startdate - timedelta(days=30)
  pr=purchase_record_model.objects.filter(created__lte=enddate)
  pr.delete()
  user=User.objects.get(id=request.user.id)
  pr=user.pr_usernameOf.all()
  context={
    'pr':pr
  }
  return render(request,'purchase_record.html',context)