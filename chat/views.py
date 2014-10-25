#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives   
from chat.models import t_user_info
import random
import re

#注册
def register(request):
	print "进入注册","sss"
	if request.method == 'POST':
		print "进入注册","tt"
		uid = rand()
		print uid,"uid是"
		name = request.POST.get('name','')
		password = request.POST.get('password','')
		email = request.POST.get('email','')
		tel = request.POST.get('tel','')
		register_date = request.POST.get('register_date','')
		print "tt",name,password,email,tel,register_date
		userObj = t_user_info(
			user_id = uid,
			user_name = name,
			user_password = password,
			user_sex = '1',
			user_age = '20',
			user_birthday = '2000-05-05',
			user_mail = email,
			user_area = '北京',
			user_register_date = register_date,
			user_tel = tel)
		userObj.save()
		print "注册成功"
		return HttpResponse(uid)
	return HttpResponse('服务器错误')

#登陆验证
def loginValidate(request):
	if request.method == 'POST':
		user_mail = request.POST.get('uid_mail','')
		password = request.POST.get('password','')
		print "post message",user_mail,password
		if("@" in user_mail):
			try:
				obj = t_user_info.objects.get(user_mail = user_mail,user_password = password)
				return HttpResponse('登陆成功')
			except t_user_info.DoesNotExist:
				return HttpResponse('邮箱与密码不匹配！请确认后再输入！')
		else:
			try:
				obj = t_user_info.objects.get(user_id = user_mail,user_password = password)
				return HttpResponse('登陆成功')
			except t_user_info.DoesNotExist:
				return HttpResponse('chat号与密码不匹配！请确认后再输入！')
	

#生成数据库中没有的六位整数
def rand():
	while(True):
		uid = random.randint(100001,999999)
		print uid
		if (re.search('^.*?[^0]$', str(uid))):
			print "生成的是：",uid,"即将查询数据库中是否存在"
			try:
				obj = t_user_info.objects.get(user_id = uid)
			except t_user_info.DoesNotExist:
				return uid

