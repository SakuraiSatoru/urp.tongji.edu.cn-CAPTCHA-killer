import urllib2
import time


def dw(i):
    result = urllib2.urlopen('http://urp.tongji.edu.cn/captchaGenerate.portal?s=')
    
    print 'sents'
    rere = result.read()
    time.sleep(0)
    local = open (str(i)+'.jpg','wb')
    local.write(rere)
    local.close()

    print i,'done'
i = 390
while i <= 1000:
    dw(i)
    i = i + 1
print 'all done'
