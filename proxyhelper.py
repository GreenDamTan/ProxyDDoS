#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import re
import proxypool
import useragenthelper

class ProxyCollect(object):
    def get(self):
        pass

class FormLiunianip(ProxyCollect):
    @classmethod
    def get(Class):
        ret = []
        try:
            r = requests.get('http://www.89ip.cn/api/api.php?&tqsl=500&sxa=&sxb=&tta=&ports=&ktip=&cf=1', timeout = 10)
            for i in re.findall('(\d+.\d+.\d+.\d+):(\d+)', r.text):
                ret.append(proxypool.Proxy(i[0], i[1]))
            print 'Get %s proxy from Liunian' % str(len(ret))
        except:
            #import traceback
            #print traceback.print_exc()
            pass
        return ret

class Form66ip(ProxyCollect):
    @classmethod
    def get(Class):
        ret = []
        try:
            headers = {'User-Agent': useragenthelper.get()}
            r = requests.get('http://66ip.cn/nmtq.php?getnum=500&isp=0&anonymoustype=4&start=&ports=&ipaddress=&area=0&proxytype=0&proxytype=1&api=71daili', timeout = 10, headers=headers)
            for i in re.findall('(\d+.\d+.\d+.\d+):(\d+)', r.text):
                ret.append(proxypool.Proxy(i[0], i[1]))
            print 'Get %s proxy from Form66ip' % str(len(ret))
        except:
            pass
        return ret

class ProxyHelper(object):

    instance = None

    @staticmethod
    def get_instance():
        if ProxyHelper.instance is None:
            ProxyHelper.instance = ProxyHelper()
        return ProxyHelper.instance

    @classmethod
    def GetFormUrl(Class, _ProxyCollect):
        return _ProxyCollect.get()

def test():
    ph = ProxyHelper.get_instance()
    ph.GetFormUrl(Form66ip)
    ph.GetFormUrl(FormLiunianip)
#()
