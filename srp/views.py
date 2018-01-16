# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from xml.etree.ElementTree import ElementTree
from django.http import HttpResponseRedirect, Http404,HttpResponse
from django.urls import reverse
import xml.etree.ElementTree as ET

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from urllib import urlopen
import urllib2

import re
# Create your views here.

#网址ip和domain
site_ip = '222.16.42.167'
site_main = 'wdesign'

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

#遍历资源xml来获得数据，没有用到dfs(只是起初取了dfs)
def dfs_for_data(root_node, level, result_list,res_type,res_head):  
    xml_ns = ''
    if res_type == 'resources_Database.xml':
    	xml_ns = '{http://tempuri.org/resources_Database.xsd}'
    elif res_type == 'videos_Database.xml':
    	xml_ns = '{http://tempuri.org/videos_Database.xsd}'
    print xml_ns+'title'
    title_text = root_node.find(xml_ns+'title').text
    type_text = ''
    if res_type == 'resources_Database.xml':
    	type_text = root_node.find(xml_ns+'fileFormat').text
    elif res_type == 'videos_Database.xml':
    	type_text = root_node.find(xml_ns+'videoFormat').text
    ID_text = root_node.find(xml_ns+'ID').text
    download_text = res_head+root_node.find(xml_ns+'resPath').text
    
    print title_text
    print type_text
    print download_text
    print '-----------'
    temp_list =[ID_text, title_text, type_text, download_text]  
    #if level != 1 and root_node.attrib.get('hyperLinkFile', '123') != 'view_resource.htm':
    #    return
    result_list.append(temp_list)  

#处理提交，即改session,然后跳转回detail
def process_get(request):
    request.session['argStr'] = request.GET.get('argStr')
    print request.session['argStr']
    return HttpResponseRedirect(reverse('srp:detail'))

#读取数据，返回xml树节点，异常情况下在异常位置插入一个空格，避免异常编码
def read_data(xml_text):
    try:
    	rt = ET.fromstring(xml_text)
    	return rt
    	pass
    except Exception as e:
    	print '--------'
    	print e
    	error_str = re.findall(r"\d+\.?\d*",str(e))
    	e_row, e_col = int(error_str[0]), int(error_str[1])
    	# print str(e_row) + str(e_col)
    	# print e_row
    	# print e_col
    	col, row = 1, 1
    	nex_text = u""
    	for i in range(len(xml_text)):
    		if xml_text[i] == '\n': row+=1
    		if row == e_row:
    			aa = xml_text[0:(i+e_col+2)]#错之前
    			bb = str('#32;')     #空格
    			cc = xml_text[(i+e_col+2):len(xml_text)]#错之后
    			# print type(aa)
    			# print type(bb)
    			# print type(cc)
    			nex_text = aa+bb+cc
    			#nex_text = xml_text[0:(i+e_col+2)]+u'#32'+xml_text[(i+e_col+2):len(xml_text)]
    			#print xml_text[(i+e_col):(i+e_col+4)]+u'@@@@@@@@'
    			break
    	#print nex_text.decode('utf-8').encode('gbk')
    	#rt = ET.fromstring(nex_text)
    	#return rt
    	return read_data(nex_text)
    	#print row
    	#raise
    else:
    	pass
    finally:
    	pass

#从xml_path中解析数据
def get_xml_data(xml_path):
    url_path = 'http://'+site_ip+'/'+xml_path
    print url_path
    #url_path = urllib.quote(url_path.encode('utf8'), ':/')

    res_type = xml_path.split('/')[-1]
    url_path=url_path.encode('utf-8')
    url_path=urllib2.unquote(url_path)

    res_head =  'http://'+site_ip+'/'+'/'.join(xml_path.split('/')[:-1])+'/'
    print '--------'
    
    #打开url数据
    data = urlopen(url_path)#.read().decode('ascii', 'ignore')  
    #data = 'srp/static/videos_Database.xml'
    #data_tree = ElementTree()
    #data_text = data
    data_text = data.read()
    #data_text = "<title>Social Communication&#xB;&amp; SMAS</title>"
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    #print data_text.decode('utf-8').encode('utf8')
    #print data_text.decode('utf-8').encode('gbk')
    dd = data_text#.decode('utf-8').encode('gbk')
    #print dd
    #data = data.encode('utf8')
    #rt = data_tree.parse(data_text)

    #parser = ET.XMLParser(encoding="utf-8")
    #rt = ET.fromstring(dd, parser=parser)
    #rt = read_data(data_text)
    #rt = ET.parse(dd)
    #with open(data,'r') as f:
    #    dd = f.read()
    rt = read_data(dd)
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


    L = get_xml_data(xml_path)     #获得数据
    L = list(reversed(L))      #反转列表
    
    #以下是分页操作
    paginator = Paginator(L, 5) # Show 10 contacts per page

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

#默认页面下，先写一个默认的session，避免detail中未设session报错
def index(request):
    request.session['argStr'] = '3|0|0|0'
    return render(request,'index.html')


