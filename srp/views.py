# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from xml.etree.ElementTree import ElementTree
from django.http import HttpResponseRedirect, Http404,HttpResponse
from django.urls import reverse

from urllib import urlopen
import urllib2
# Create your views here.

site_ip = '222.16.42.167'
site_main = 'wdesign'

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

def dfs_for_data(root_node, level, result_list,res_type):  
    xml_ns = ''
    if res_type == 'resources_Database.xml':
    	xml_ns = '{http://tempuri.org/resources_Database.xsd}'
    elif res_type == 'videos_Database.xml':
    	xml_ns = '{http://tempuri.org/videos_Database.xsd}'
    print xml_ns+'title'
    title_text = root_node.find(xml_ns+'title').text
    type_text = ''
    if res_type == 'view_resource.htm':
    	type_text = root_node.find(xml_ns+'type').text
    elif res_type == 'video_resources.aspx':
    	type_text = root_node.find(xml_ns+'videoFormat').text
    ID_text = root_node.find(xml_ns+'ID').text
    
    print title_text
    print '-----------'
    temp_list =[ID_text, title_text, type_text]  
    #if level != 1 and root_node.attrib.get('hyperLinkFile', '123') != 'view_resource.htm':
    #    return
    result_list.append(temp_list)  

def process_get(request):
    print '切换分支'
    request.session['argStr'] = request.GET.get('argStr')
    print request.session['argStr']
    return HttpResponseRedirect(reverse('srp:detail'))

def get_xml_data(xml_path):
    url_path = 'http://'+site_ip+'/'+xml_path
    print url_path
    #url_path = urllib.quote(url_path.encode('utf8'), ':/')

    res_type = xml_path.split('/')[-1]
    url_path=url_path.encode('utf-8')
    url_path=urllib2.unquote(url_path)
    #print url_path
    data = urlopen(url_path)#.read().decode('ascii', 'ignore')  
    #data = 'srp/static/resources_Database.xml'
    data_tree = ElementTree()
    rt = data_tree.parse(data)
    res = []
    res_node = rt.getchildren()
    for i in res_node:
        dfs_for_data(i,0,res,res_type)
    return res

def detail(request):
    ss = request.session['argStr']
    node_str = ss.split('|')
    node_list =[]
    for i in node_str:
    	node_list.append(int(i))

    tree = ElementTree()
    file_name = 'srp/static/menu.xml'
    root = tree.parse(file_name)
    xml_path = dfs_for_xml(root, node_list)


    L = get_xml_data(xml_path)
    
    return render(request,'detail.html',{'L':L})


def index(request):
    request.session['argStr'] = '3|0|0|0'
    return render(request,'index.html')


