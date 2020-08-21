from urllib.request import urlretrieve
from urllib.request import  urlopen
from bs4 import BeautifulSoup
from numpy import arange
import re
import os
def cbk(a,b,c):
    '''''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    per=100.0*a*b/c
    if per>100:
        per=100
    print( '%.2f%%' % per)

shutpoint = 2012078041643   #########################################

dir=os.path.abspath('.')
html = urlopen("https://oceandata.sci.gsfc.nasa.gov/GOCI/L2")
bsobj = BeautifulSoup(html, "lxml")
#print(bsobj)
year = arange(2012,2019,1)
for yearnum in year:
    for link in bsobj.find("div",{"id":"main"}).findAll("a",href = re.compile("/GOCI/L2/"+str(yearnum)+"/*$")):
        print(link.attrs['href'])
        html1 = urlopen("https://oceandata.sci.gsfc.nasa.gov"+link.attrs['href'])
        bsobj1 = BeautifulSoup(html1, "lxml")
        #print(bsobj1)

        for link1 in bsobj1.find("div",{"id":"main"}).findAll("a",href = re.compile("^/GOCI/L2/"+str(yearnum)+"/.*")):
            daynum = int(link1.attrs['href'][-9:-5] + link1.attrs['href'][-4:-1]) ###################### 拼接年份+日数转整形
            if daynum>=int(shutpoint/1e6):
                html2 = urlopen("https://oceandata.sci.gsfc.nasa.gov"+link1.attrs['href'])
                bsobj2 = BeautifulSoup(html2, "lxml")
                #print(bsobj2)

                for link2 in bsobj2.find("div",{"id":"main"}).findAll("a",href = re.compile(".*\.L2_COMS_OC\.nc$")):
                    print(link2.attrs['href'])
                    filenum = int(link2.attrs['href'][-27:-14])
                    if filenum>=shutpoint:
                        print(filenum)
                        urlretrieve(link2.attrs['href'],filename=dir+'\\'+link2.attrs['href'][-28:],reporthook=cbk)
