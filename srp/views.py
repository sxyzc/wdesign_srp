# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from xml.etree.ElementTree import ElementTree
from django.http import HttpResponseRedirect, Http404,HttpResponse
from django.urls import reverse
import xml.etree.ElementTree as ET

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from urllib import urlopen
import urllib2

import re

from .models import Res
# Create your views here.

#网址ip和domain
site_ip = '222.16.42.167'
site_main = 'wdesign'

#遍历所有的节点  
def dfs_for_database_menu(root_node, xml_path):
    node_name = root_node.attrib.get('displayName', site_main)
    #if level != 1 and root_node.attrib.get('hyperLinkFile', '123') != 'view_resource.htm':
    #    return
    
    #遍历每个子节点  
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        
        xml_suffix = ""
        if root_node.attrib['hyperLinkFile'] == 'view_resource.htm':
        	xml_suffix = 'resources_Database.xml'
        elif root_node.attrib['hyperLinkFile'] == 'video_resources.aspx':
        	xml_suffix = 'videos_Database.xml'
        if xml_suffix == "":
        	return
        xml_path = xml_path + node_name + "/" + xml_suffix

        L = get_xml_data(xml_path)
        for i in L:
        	#Res.objects.create(res_name=i.title_text,res_path=i.download_text,res_format=i.format_text,res_size=i.size_text,create_time=i.time_text,upload_user=i.user_text,key_word=i.key_word,other_01=i.other_01,other_02=i.other_02,other_03=i.other_03)
        	Res.objects.create(res_name=i[0],res_path=i[1],res_format=i[2],res_size=i[3],create_time=i[4],upload_user=i[5],key_word=i[6],other_01=i[7],other_02=i[8],other_03=i[9])
        
        return
    for child in children_node:
        dfs_for_database_menu(child, xml_path+node_name + "/")
    return

#使用dfs来深搜menu，返回一条到底的路径string
def dfs_for_xml(root_node, node_list):
    node_name = root_node.attrib.get('displayName', site_main)
    #node_name = root_node.attrib['displayName']

    children_node = root_node.getchildren()  
    if len(children_node) == 0:
        xml_suffix = ""
        if root_node.attrib['hyperLinkFile'] == 'view_resource.htm':
        	xml_suffix = 'resources_Database.xml'
        elif root_node.attrib['hyperLinkFile'] == 'video_resources.aspx':
        	xml_suffix = 'videos_Database.xml'
        
        return node_name + "/" + xml_suffix

    elif len(node_list) == 0:
    	return node_name + "/" + dfs_for_xml(children_node[0],node_list)
    else :#elif len(node_list) != 0:
    	return node_name + "/" + dfs_for_xml(children_node[node_list[0]],node_list[1:])

def get_text(root_node,attrib_name):
    temp = root_node.find(attrib_name)
    if temp == None:
    	return ""
    else:
    	if temp.text == None:
    		return ""
    	return temp.text

#遍历资源xml来获得数据，没有用到dfs(只是起初取了dfs)
def dfs_for_data(root_node, level, result_list,res_type,res_head):
    xml_ns = ''
    if res_type == 'resources_Database.xml':
    	xml_ns = '{http://tempuri.org/resources_Database.xsd}'
    elif res_type == 'videos_Database.xml':
    	xml_ns = '{http://tempuri.org/videos_Database.xsd}'
    print xml_ns+'title'
    #title_text = root_node.find(xml_ns+'title').text
    title_text = get_text(root_node, xml_ns+'title')
    
    format_text = ''
    if res_type == 'resources_Database.xml':
    	format_text = get_text(root_node, xml_ns+'fileFormat')
    	#format_text = root_node.find(xml_ns+'fileFormat').text
    elif res_type == 'videos_Database.xml':
    	#format_text = root_node.find(xml_ns+'videoFormat').text
    	format_text = get_text(root_node, xml_ns+'videoFormat')
    #ID_text = root_node.find(xml_ns+'ID').text
    #download_text = res_head+root_node.find(xml_ns+'resPath').text
    #other_01 = res_head+'showResources.aspx?resPath='+root_node.find(xml_ns+'resPath').text+'&uploadMode=singleFile(wmv)'
    
    download_text = res_head + get_text(root_node, xml_ns+'resPath')
    other_01 = res_head+'showResources.aspx?resPath='+get_text(root_node, xml_ns+'resPath')+'&uploadMode=singleFile(wmv)'
    
    size_text = get_text(root_node, xml_ns+'resSize')
    other_02 = get_text(root_node, xml_ns+'teacher')
    other_03 = get_text(root_node, xml_ns+'teachingFilePath')
    time_text = get_text(root_node, xml_ns+'createTime')
    user_text = get_text(root_node, xml_ns+'uploadUser')
    key_word = get_text(root_node, xml_ns+'keyWord')
    
    # size_text = root_node.find(xml_ns+'resSize').text
    # other_02 = root_node.find(xml_ns+'teacher').text
    # other_03 = root_node.find(xml_ns+'teachingFilePath').text
    # time_text = root_node.find(xml_ns+'createTime').text
    # user_text = root_node.find(xml_ns+'uploadUser').text
    # key_word = root_node.find(xml_ns+'keyWord').text
    
    print '-----------'
    temp_list =[title_text,download_text,format_text,size_text,time_text,user_text,key_word,other_01,other_02,other_03]  
    #print temp_list
    #if level != 1 and root_node.attrib.get('hyperLinkFile', '123') != 'view_resource.htm':
    #    return
    result_list.append(temp_list)  

#遍历资源xml来获得数据，没有用到dfs(只是起初取了dfs)
def dfs_for_news(root_node, result_list):
    #title_text = root_node.find(xml_ns+'title').text
    title_text = root_node.find('title').text
    link_text = root_node.find('hyperLinkFile').text
    time_text = root_node.find('createTime').text
    

    print '-----------   news'
    temp_list =[title_text,link_text,time_text]  
    print temp_list
    #print temp_list
    #if level != 1 and root_node.attrib.get('hyperLinkFile', '123') != 'view_resource.htm':
    #    return
    result_list.append(temp_list)  


#处理提交，即改session,然后跳转回detail
def process_get(request):
    request.session['argStr'] = request.GET.get('argStr')
    print '处理提交：' + request.session['argStr']
    print request.GET.get('argStr').split('|')[0]
    if request.GET.get('argStr').split('|')[0] == '1':
        return HttpResponseRedirect(reverse('srp:introduce'))#为课程简介
    return HttpResponseRedirect(reverse('srp:detail'))


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#回到列表界面
def introduce(request):
    print '测试简介'
    

    ss = request.session['argStr']
    node_str = ss.split('|')
    node_list =[]
    for i in node_str:
        node_list.append(int(i))

    tree = ElementTree()
    file_name = 'srp/static/menu.xml'
    root = tree.parse(file_name)
    
    xml_path = dfs_for_xml(root, node_list)    #读menu.xml来获得xml路径
    if xml_path.split('/')[-1] != u'':
        return HttpResponseRedirect(reverse('srp:detail'))
    
    print '@@@@@@@@@@@@@'
    print xml_path 

    print xml_path.split('/')
    title_text=xml_path.split('/')[-2]

    print title_text
    url_path = 'http://'+site_ip+'/'+xml_path
    
    print url_path

    res_type = xml_path.split('/')[-1]
    url_path=url_path.encode('utf-8')
    url_path=urllib2.unquote(url_path)

    res_head =  'http://'+site_ip+'/'+'/'.join(xml_path.split('/')[:-1])+'/'
    print '--------'
    print url_path.decode('utf-8')
    #打开url数据
    data = urlopen(url_path)#.read().decode('ascii', 'ignore')  
    
    data_text = data.read().decode('gbk')

    si = data_text.find(u"<body>")+6
    ti = data_text.find(u"</body>")
    print si,ti
    print data_text[si:ti]

    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'

    res_text=data_text[si:ti]

    
    

    return render(request,'introduce.html',{'introduction':res_text,'title_text':title_text})

def viewer(request):
    print '处理viewerjs：'
    filename = request.GET.get('filename')
    #request.META['Access-Control-Allow-Origin']='*'
    template = loader.get_template('viewer.html')
    response = HttpResponse(template.render({'filename':filename}, request))
    response['Access-Control-Allow-Origin']='*'
    print filename
    response['Access-Control-Allow-Origin'] = '*' 
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS' 
    response['Access-Control-Max-Age'] = '1000' 
    response['Access-Control-Allow-Headers'] = '*' 
    return response
    #return render(request,"viewer.html",{'filename':filename})

#处理搜索请求
def process_search(request):
    
    keyword = request.GET.get('keyword')
    print '处理搜索'
    L = []
    if keyword != None and keyword!="":
        request.session['search_key'] = keyword
    else:
        keyword = "e6f135cc18852da1afd51f4f7d420905"   #不可能成为关键字的字符串就行，这里是一个字符串的md5
    
    res = Res.objects.all()
    for i in res:
    	if i.res_name.count(keyword) > 0:
    		L.append(i)

    #以下是分页操作
    paginator = Paginator(L, 10) # 每页10条

    page = request.GET.get('page')
    if page is None:
    	page = 1
    print page
    try:
        ress = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ress = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ress = paginator.page(paginator.num_pages)
    return render(request,'search.html',{'L':ress,'search_key':keyword})

#读取数据，返回xml树节点，异常情况下在异常位置插入一个空格，避免异常编码
#这是为了解决在视频库中遇到错误xml文件编码的bug
def read_data(xml_text):
    try:
    	rt = ET.fromstring(xml_text)
    	return rt
    	pass
    except Exception as e:
    	print '解析xml遇到异常，尝试处理！'
    	print e
    	error_str = re.findall(r"\d+\.?\d*",str(e))
    	e_row, e_col = int(error_str[0]), int(error_str[1])
    	col, row = 1, 1
    	nex_text = u""
    	for i in range(len(xml_text)):
    		if xml_text[i] == '\n': row+=1
    		if row == e_row:
    			aa = xml_text[0:(i+e_col+2)]#错之前
    			bb = str('#32;')     #空格
    			cc = xml_text[(i+e_col+2):len(xml_text)]#错之后
    
    			nex_text = aa+bb+cc
    
    			break
    	
    	return read_data(nex_text)
    else:
    	pass
    finally:
    	pass

#从xml_path中解析数据
def get_xml_data(xml_path):
    url_path = 'http://'+site_ip+'/'+xml_path
    
    print url_path

    res_type = xml_path.split('/')[-1]
    url_path=url_path.encode('utf-8')
    url_path=urllib2.unquote(url_path)

    res_head =  'http://'+site_ip+'/'+'/'.join(xml_path.split('/')[:-1])+'/'
    print '--------'
    
    #打开url数据
    data = urlopen(url_path)#.read().decode('ascii', 'ignore')  
    
    data_text = data.read()
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    
    #with open('srp/static/videos_Database.xml','r') as f:
    #    data_text = f.read()
    rt = read_data(data_text)
    res = []
    res_node = rt.getchildren()
    for i in res_node:
        dfs_for_data(i,0,res,res_type,res_head)
    return res

#回到列表界面
def detail(request):
    ss = request.session['argStr']
    node_str = ss.split('|')
    node_list =[]
    for i in node_str:
    	node_list.append(int(i))

    tree = ElementTree()
    file_name = 'srp/static/menu.xml'
    root = tree.parse(file_name)
    
    xml_path = dfs_for_xml(root, node_list)    #读menu.xml来获得xml路径
    request.session['cat_path'] = '/'.join(xml_path.split('/')[1:-1])

    L = get_xml_data(xml_path)     #获得数据
    L = list(reversed(L))      #反转列表
    
    #以下是分页操作
    paginator = Paginator(L, 10) # 每页10条

    page = request.GET.get('page')
    if page is None:
    	page = 1
    print page
    try:
        ress = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ress = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ress = paginator.page(paginator.num_pages)

    #return render(request,'detail.html',{'L':L})
    return render(request,'detail.html',{'L':ress})

def get_news_or_recommend(data_url):
    data = urlopen(data_url)#.read().decode('ascii', 'ignore')  
    
    data_text = data.read()
    rt = read_data(data_text)
    res = []
    res_node = rt.getchildren()
    for i in res_node:
        dfs_for_news(i,res)
    return res

#默认页面下，先写一个默认的session，避免detail中未设session报错
def index(request):
    #request.session['argStr'] = '3|0|0|0'
    #data = urlopen()#.read().decode('ascii', 'ignore')  
    news_L = get_news_or_recommend('http://222.16.42.167/wdesign/%E9%A6%96%E9%A1%B5/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A/linkTitle.xml')
    recommend_L = get_news_or_recommend('http://222.16.42.167/wdesign/%E9%A6%96%E9%A1%B5/%E6%8E%A8%E8%8D%90%E9%98%85%E8%AF%BB/linkTitle.xml')
    return render(request,'index.html',{'newsList':news_L[:5],'recList':recommend_L[:5]})

def update_data(request):
    print '更新数据，先删除数据'
    L = Res.objects.all()
    for i in L:
    	i.delete()
    print '删除数据完毕，准备更新'
    tree = ElementTree()
    file_name = 'srp/static/menu.xml'
    root = tree.parse(file_name)
    dfs_for_database_menu(root,'/')
    print '更新完成'
    return render(request,'index.html')
