from urllib.request import urlretrieve
from urllib.request import  urlopen
from bs4 import BeautifulSoup
import re
import os

def cbk(a,b,c):
    '''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    per=100.0*a*b/c
    if per>100:
        per=100
    print( '%.2f%%' % per)
    
# shutpoint = 2012078041643   #########################################

dir=os.path.abspath('.')
html = urlopen("http://222.236.46.45/nfsdb/COMS/GOCI/2.0/")
bsobj = BeautifulSoup(html, "lxml")
tag = bsobj.find_all(re.compile("a"))
#print(tag[6])
#print(bsobj)
#year = arange(1948,2020,1)
year = [2020]

for yearnum in year:
    path = dir + '/' + str(yearnum)
    if not os.path.isdir(path): 
        os.makedirs(path) 
    address = bsobj.find_all("a",href=re.compile("/GOCI/2.0/"+str(yearnum)))[0]
    #print( address.get('href') )
    #print(address.get('href'))
    
    html1 = urlopen("http://222.236.46.45" + address.get('href')  )
    bsobj1 = BeautifulSoup(html1, "lxml")
    monthnumber = len(bsobj1.find_all("a"))-1
    
    for m in range(1):
        address2 = bsobj1.find_all("a")[m+1].get('href') 
        html2 = urlopen("http://222.236.46.45" + address2 )
        bsobj2 = BeautifulSoup(html2, "lxml")
        #print(bsobj2)
        daynumber = len(bsobj2.find_all("a"))-1
        
        for d in range(1):
            address3 = bsobj2.find_all("a")[d+1].get('href') 
            html3 = urlopen("http://222.236.46.45" + address3 + 'L2/' )
            bsobj3 = BeautifulSoup(html3, "lxml")
            print( len(bsobj3.find_all("a"))-1 ) 
            
            for f in range(1):
            #range( len(bsobj3.find_all("a"))-1 ):
                address4 = bsobj3.find_all("a")[f+1].get('href') 
                url = "http://222.236.46.45" + address4    
                filname = address4[address4.rindex('/'):]
                print(path+filname)
                urlretrieve(url,path+filname, reporthook=cbk)
