# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Res(models.Model):
	res_name = models.CharField(max_length=60)
	res_path = models.CharField(max_length=100)

	res_format = models.CharField(max_length=20)
	res_size = models.CharField(max_length=20)
	create_time = models.CharField(max_length=30)
	upload_user = models.CharField(max_length=30)
	key_word = models.CharField(max_length=100)

	other_01 = models.CharField(max_length=100)
	other_02 = models.CharField(max_length=100)
	other_03 = models.CharField(max_length=100)
	
	
	def __str__(self):
		return self.res_name