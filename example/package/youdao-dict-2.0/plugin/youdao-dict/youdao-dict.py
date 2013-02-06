#!/usr/bin/env python
import urllib2
import urllib
import json
import sys
import os 
import subprocess  
import vim


use_local_dict=1
local_dict="sdcv"

use_network_youdao=1
# put your youdao api key here, you should keep it secret
youdao_key = '1845492630'
# put your youdao api keyfrom here
youdao_keyfrom = 'howlanderson'

word = sys.argv[1]

dict_output=""
youdao_output=""

if use_local_dict:
    for cmdpath in os.environ['PATH'].split(':'):
        if os.path.isdir(cmdpath) and local_dict in os.listdir(cmdpath):
            use_local_dict=1

    if use_local_dict:          
        dict_output = subprocess.Popen(["sdcv", "-n", word], stdout=subprocess.PIPE).communicate()[0]
        print dict_output

if use_network_youdao:
    youdao_url = 'http://fanyi.youdao.com/openapi.do?keyfrom=' + youdao_keyfrom + '&key=' + youdao_key + '&type=data&doctype=json&version=1.1&q=' + word
    try:
        req = urllib2.Request(url = youdao_url)
        f = urllib2.urlopen(req)
        json_data = f.read()
        json_object = json.loads(json_data)
    except Exception, e:
        #print 'some error happened'
        sys.exit()
    if not json_object['errorCode']: 
        try:
            translation_result = json_object['basic']['explains']
        except Exception, e:
            #print 'some error happened'
            sys.exit()
        youdao_output = (''.join(translation_result)).encode('utf-8', 'ignore')
        print "\n===youdao===\n" + youdao_output
    else:
        #print 'api return error'
        pass
