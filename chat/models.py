#coding:utf-8
from django.db import models

# Create your models here.
import simplejson as json
# Create your models here.

'''
用户表 
'''
class t_user_info(models.Model):
	user_id = models.CharField(max_length=16,verbose_name='用户账号',unique=True)
	user_name = models.CharField(max_length=128,verbose_name='用户名')
	user_password= models.CharField(max_length=16,verbose_name='密码')
	user_tel = models.CharField(max_length=30,verbose_name='联系电话',null=True)
	user_mail = models.EmailField(verbose_name='邮箱')
	user_sex = models.IntegerField(max_length=16,verbose_name='性别',null=True)
	user_age = models.IntegerField(max_length=30,verbose_name='年龄',null=True)
	user_birthday = models.DateField(verbose_name='出生日期',null=True)
	user_area = models.CharField(max_length=256,verbose_name='用户地区',null=True)
	user_register_date = models.DateField(verbose_name="注册日期")
	def __unicode__(self):
		return self.user_name

	class Meta:
		verbose_name = '用户'
		verbose_name_plural = '用户表'



'''
好友表 
'''

class t_user_friend(models.Model):
	user_id = models.ForeignKey(t_user_info,verbose_name="用户账号")
	user_friend = models.CharField(max_length=256,verbose_name='好友',null=True)
	def __unicode__(self):
		return self.user_id

	class Meta:
		verbose_name = '好友表'
		verbose_name_plural = '好友表'


'''
所在群
'''

class t_user_group(models.Model):
	user_id = models.ForeignKey(t_user_info,verbose_name="用户账号")
	user_friend = models.CharField(max_length=256,verbose_name='群',null=True)
	def __unicode__(self):
		return self.user_id

	class Meta:
		verbose_name = '所在群表'
		verbose_name_plural = '所在群表'


'''
心情
'''

class t_user_xinqing(models.Model):
	user_id = models.ForeignKey(t_user_info,verbose_name="用户账号")
	user_xinqing = models.CharField(max_length=512,verbose_name='群',null=True)
	def __unicode__(self):
		return self.user_id

	class Meta:
		verbose_name = '用户心情'
		verbose_name_plural = '用户心情'