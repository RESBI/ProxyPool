import requests
import re
import time
import _thread
import random
import os
import ssl

Htmlpath = "/var/www/html/proxypool/"

def Out(mode,types,end="\n"):
    modes = ["Ok","Wr","Er","Nt"]
    colos = ["92","93","95","91"]
    if mode in modes:
        for cou in range(len(modes)):
            if mode == modes[cou]:
                print("\033[1;"+colos[cou]+"m"+str(types),end=end)
                break
    else:
        Out("Er","No this mode: "+mode)

def getHtml(Url, p = 0):
    ssl._create_default_https_context = ssl._create_unverified_context
    headers = dict()
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 '
    if p:
        proxies = { "http"  : p,
                    "https" : p }
        response = requests.get(Url, headers=headers, proxies = proxies, timeout = 30)
    else:
        response = requests.get(Url, headers=headers, timeout = 30)
    response.encoding = 'UTF-8'
    html = response.text
    response.close()
    return html

def getRe(pattern, data):
    result = re.findall(pattern, data, re.S)
    return result

def getXiCi(page = random.randint(11, 1000)):
    Out("Wr", "Getting Xici...")
    pattern = r'''<img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\n      <td>(.*?)</td>\n      <td>(.*?)</td>\n      <td>\n        <a href="\S+">(.*?)</a>\n      </td>\n      <td class="country">高匿</td>\n      <td>(.*?)</td>\n      <td class="country">\n        <div title="\S+秒" class="bar">'''
    
    result = []
    #howMANY = int(input("How many pages do you want?: "))
    for n in range(page - 10, page + 1):
        Out("Nt", " {}".format(n), "\r")
        try:
#            Out("Nt", "Getting page {}...".format(n), "\t")
            data = getHtml('http://www.xicidaili.com/nn/{}'.format(n))
            result += getRe(pattern, data)
#            Out("Ok", "Done! total URLs : {}".format(len(result)), "\r")
            time.sleep(10)
        except:
            continue
#    Out("Ok", "Total get: {}{}".format(len(result), " "*10))
    get = []
    for k in result:
        (a, b, c, d) = k
        d = d.lower()
        m = "{}://{}:{}\n".format(d, a, b)
        if m in get:
            pass
        else:
            get += [m]
    return get

def get66ip(proxy_number=1000):
    Out("Wr", "Getting 66ip...")
    url = "http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(proxy_number)
    data = getHtml(url)
    result = getRe(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', data)
    res = []
    for k in result:
        k1 = "http://{}".format(k)
        k2 = "https://{}".format(k)
        if not((k1 in res) or (k2 in res)):
            res += [k1, k2]
    return res

def get89ip(proxy_number=500):
    Out("Wr", "Getting 89ip...")
    url = "http://www.89ip.cn/tiqv.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1".format(proxy_number)
    data = getHtml(url)
    result = getRe(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', data)
    res = []
    for k in result:
        k1 = "http://{}".format(k)
        k2 = "https://{}".format(k)
        if not((k1 in res) or (k2 in res)):
            res += [k1, k2]
    return res

def Kuaidaili(mode = "ha", page = random.randint(11, 500)):
    Out("Wr", "Getting Kuaidaili...")
    url = "https://www.kuaidaili.com/free/in{}/{}/"
    pattern = r'''<td data-title="IP">(.*?)</td>
                    <td data-title="PORT">(.*?)</td>
                    <td data-title="匿名度">(.*?)</td>
                    <td data-title="类型">(.*?)</td>'''
    result = []
    for k in range(page - 10, page + 1):
        try:
            Out("Nt", " {}".format(k), "\r")
            gurl = url.format(mode, k)
            data = getHtml(gurl)
            res = getRe(pattern, data)
            for l in res:
                [a, b, c, d] = l
                d = d.lower()
                m = "{}://{}:{}".format(d, a, b)
                if not(m in result):
                    result += [m]
            time.sleep(10)
        except:
            c = 1
    return result

def getKuaidailign():
    result = Kuaidaili(mode = "ha")
    return result

def getKuaidailitm():
    result = Kuaidaili(mode = "tr")
    return result

def OkQ(Proxy):
    Url = "https://canihazip.com/"
    pattern = r'''<center>IP: (.*?)</center>'''    
    Url2 = "https://www.ipip.net"
    pattern2 = r'''<div class="ip_text">您当前的IP：(.*?)</div>'''
    Cap2 = ""
    Cap = ""
    try:
        get = getHtml(Url, Proxy)
        Cap = getRe(pattern, get)[0]
    except:
        try:
            get = getHtml(Url2, Proxy)
            Cap2 = getRe(pattern2, get)[0]
        except:
            return 0
    if (Cap in Proxy) or (Cap2 in Proxy):
        return 1
    else:
        return 0
#    except:
#        return 0
            #print(Cap)

ppcheck = """
def Check(proxies):
    result = []
    total = len(proxies)
    jobs = [(job_server.submit(OkQ, (proxies[m], ), (getHtml, getRe,), ("requests", "ssl", "re",)), m, proxies[m]) for m in range(len(proxies))]
    for [job, now, p] in jobs:
        Out("Ok", "Checking Proxy... OK : {} | total: {} | now: {}".format(len(result), total, now), "\r")
        Temp = job()
        if Temp:
            result += [p]
    return result
"""

def Check(proxy, limit):
    pool = 0
    res = []
    global pool
    global res
    start_time = time.time()
    def Main(Proxy, k, total):
        Out("Ok", "Checking Proxy... OK : {} | {} / {} -- {}%".format(len(res), k, total, round((k / total) * 100, 2)), "\r")
        global pool
        global res
        if OkQ(Proxy):
            res += [Proxy]
        pool -= 1
        _thread.exit()

    for k in range(len(proxy)):
        while pool > limit: pass
        _thread.start_new_thread(Main, (proxy[k], k, len(proxy)))
        pool += 1

    while 1:
        now_Time = time.time() - start_time
        if pool == 0 or now_Time > 5400:
            return res

def singleCheck(Proxies):
    result = []
    for proxy in Proxies:
        Out("Wr", "Checking {}...".format(proxy), " ")
        if OkQ(proxy):
            Out("Ok", "Success!")
            result += [proxy]
        else:
            Out("Er", "Faild!")
    Out("Ok", "Check done, There's {} useable poxy.".format(len(result)))
    return result

def toHtml(proxies, path = Htmlpath):
    https = []
    http = []
    for proxy in proxies:
        if "https" in proxy:
            https += [proxy]
        else:
            http += [proxy]
    Html = """<title>ProxyPool</title>
<html>
<br>Http:</br>
"""
    for proxy in http:
        Html += "<br>{}</br>\n".format(proxy)
    Html += """<br>-----------------</br>
<br>Https</br>
""".format(len(http))
    for proxy in https:
        Html += "<br>{}</br>\n".format(proxy)
    Html += """<br>https({}) + http({}) = {}</br>""".format(len(https), len(http), len(https)+len(http))
    f = open("{}index.html".format(path), "w+")
    f.write(Html)
    f.close()

try:
    f = open("./Proxies.txt", "r")
except:
    f = open("./Proxies.txt", "w+")
result = f.read()
f.close()
result = result.split("\n")
del(result[-1])
funcs = [getKuaidailign, getKuaidailitm, get66ip, get89ip, getXiCi]
#funcs = [get66ip]
CHECK_LIMIT = 5000
while 1:
    os.system("clear")
    temp_result = []
    Out("Nt", "Total proxies: {}.".format(len(result)))
    for getProxy in funcs:
        try:
            TEMP = getProxy()
            for k in TEMP:
                if not(k in temp_result):
                    temp_result += [k]
            Out("Ok", "Done!, {}".format(len(TEMP)))
        except:
            Out("Er", "Error!")
    result += Check(temp_result, 50)
        
    Out("Wr", "\nSaving Proxies...")
    f = open("./Proxies.txt", "w+")
    TEMP = []
    for k in result:
        if not(k in TEMP):
            f.write("{}\n".format(k))
            TEMP += [k]
    f.close()
    result = TEMP
    Out("Wr", "Saving to html...")
    toHtml(result)

    if len(result) >= CHECK_LIMIT:
        result = Check(result, 10)
        delay = 240
    else: delay = 120
    for k in range(delay):
        time.sleep(1)
        Out("Er", " Delay {}s / {}s...".format(k, delay), "\r")
    
