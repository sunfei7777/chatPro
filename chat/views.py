#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives   
from chat.models import t_user_info,t_user_friend,t_user_xinqing
import random
import re
import simplejson as json

#注册
def register(request):
	print "进入注册","sss"
	if request.method == 'POST':
		print "进入注册","tt"
		uid = rand()
		print uid,"uid是"
		name = request.POST.get('name','').encode('utf-8')
		password = request.POST.get('password','')
		email = request.POST.get('email','')
		try:
			obj = t_user_info.objects.get(user_mail = email)
			return HttpResponse("used")
		except t_user_info.DoesNotExist:
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
	return HttpResponse('坤哥滚蛋！')

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

#检索好友列表
def searchFriend(request):
	print "进入搜索好友列表"
	objxinqing = {}
	if request.method == 'POST':
		user_mail = request.POST.get('uid_mail','')
		if '@' in user_mail:
			try:
				obj = t_user_info.objects.get(user_mail = user_mail)
				uid = obj.user_id
				try:
					obj_friend = t_user_friend.objects.get(user_id = uid)
					return HttpResponse(obj_friend)
				except:
					print "未搜索到好友"
					return HttpResponse("该用户没有好友")
			except t_user_info.DoesNotExist:
				return HttpResponse("请求出错")
		else:
			try:
				obj = t_user_info.objects.get(user_id = user_mail)
				return HttpResponse(obj)
			except t_user_info.DoesNotExist:
				return HttpResponse("该用户没有好友")
			return HttpResponse("输入的是chat号")
	else:
		return HttpResponse("不可能不是post吧")

#添加好友时检索用户列表
#尼玛，这函数写的我都凌乱了，必须添加点注释啦！！o(╯□╰)o
def addSearchFriend(request):
	print "添加好友——-进入搜索好友列表"
	context_order_objs = []
	objxinqing = {}
	if request.method == 'POST':#如果为post方法，post是查询单个好友信息的，可以输入邮箱号或者chatid
		uidOrMail = request.POST.get('uidOrMail','')#获取提交到的信息
		print "到这里了",uidOrMail
		if '@' in uidOrMail:#判断是邮箱还是chatid
			try:#如果是邮箱的话进行chatid的搜索工作
				print "进入try"
				obj = t_user_info.objects.get(user_mail = uidOrMail)
				print "第一步搜索结果：",obj.user_area
				uidOrMail = obj.user_id#将邮箱号转为chat号
				print "第er步搜索结果：",uidOrMail
			except t_user_info.DoesNotExist:
				return HttpResponse("无此用户信息")
		try:
			obj =t_user_info.objects.get(user_id = uidOrMail)#用chatid搜索用户信息
			print "第er步搜索结果：",obj
			offer_obj = {}#封装成字典
			offer_obj['name'] = obj.user_name
			offer_obj['chatNum'] = obj.user_id
			try:#把心情提取出来，封装到一起
				objxinqing = t_user_xinqing.objects.get(user_id = obj.user_id)
				offer_obj['xinqing'] = objxinqing["user_xinqing"]
				print offer_obj
				context_order_objs.append(offer_obj)
				return HttpResponse(json.dumps(context_order_objs),content_type="application/json")
			except:#若果没有心情记录则添加"我还没有添加心情噢"
				objxinqing["user_xinqing"] = "我还没有添加心情噢"
				offer_obj['xinqing'] = objxinqing["user_xinqing"]
				context_order_objs.append(offer_obj)
				return HttpResponse(json.dumps(context_order_objs),content_type="application/json")
		except:
			return HttpResponse("系统错误")							

	else:
		uidOrMail = request.GET.get('uidOrMail','')
		if '@' in uidOrMail:
			objects = t_user_info.objects.get(user_mail = uidOrMail)
			uidOrMail = objects.user_id
		objects = t_user_info.objects.exclude(user_id = uidOrMail)[:5]
		for obj in objects:
			offer_obj = {}
			offer_obj['name'] = obj.user_name
			offer_obj['chatNum'] = obj.user_id
			try:
				objxinqing = t_user_xinqing.objects.get(user_id = obj.user_id)
			except:
				objxinqing["user_xinqing"] = "我还没有添加心情噢"
			offer_obj['xinqing'] = objxinqing["user_xinqing"]
			context_order_objs.append(offer_obj)
		return HttpResponse(json.dumps(context_order_objs),content_type="application/json")