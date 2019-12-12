import re
import time, timeit
import shelve
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

start=timeit.default_timer()
transregex=re.compile(r'"(.*)"\s*=\s*"(.*)";',re.DOTALL)

print('Processing, this may(will) take a while...')

textfile = open('mainfile1.txt')
list1 = textfile.readlines()
kvdict = {}
langcode='es'
outfile=open('testout1.txt','w')

while '\n' in list1:
    list1.remove('\n')
list2=[x.strip() for x in list1]

for item in list2:
    total=transregex.search(item)
    kvdict[total.group(1)]=total.group(2)

translistkeys =[]
for key in kvdict.keys():
    translistkeys.append(key)
translistvals =[]
for val in kvdict.values():
    translistvals.append(val)

newvals=[]
for item in translistvals:
    if '\\n' in item:
        item=item.split('\\n')
    newvals.append(item)

sepdict={}
for (k,v) in zip(translistkeys,newvals):
    sepdict[k] = v

options = Options()
options.set_headless()
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
assert options.headless
driver=webdriver.Firefox(firefox_options=options,firefox_profile=firefox_profile)
driver.get("https://translate.google.co.uk/#en/"+langcode+"/")


newrefvals=[]
itemlist=list(sepdict.items())
for key,value in sepdict.items():
    x=False
    if(type(value) is list):
        tempvals=[]
        for item in value:
            sepval=item
            maintext=driver.find_element_by_css_selector('.goog-textarea')
            maintext.send_keys(sepval)
            time.sleep(3)
            resultz=driver.find_elements_by_css_selector('.tlid-translation>span')
            if len(resultz)!= 0:
                tran=resultz[0].text
                tempvals.append(tran)
                maintext.clear()
                x=True
        if x:
            newstr="\\n".join(tempvals)
            sepdict[key]=newstr
        else:
            print("Not processed>> "+key+" : "+"\\n".join(value))
    else:
        rval=str(value).split(" ")
        refval=' '.join(rval)
        maintext=driver.find_element_by_css_selector('.goog-textarea')
        maintext.send_keys(refval)
        time.sleep(3)
        resultz=driver.find_elements_by_css_selector('.tlid-translation>span')
        if len(resultz)!= 0:
            tran=resultz[0].text
            sepdict[key]=tran
            maintext.clear()
        else:
            print("Not processed>> "+key+" : "+value)
    maintext.clear()
    
    num=itemlist.index((key,value))+1
    percenum=num/len(itemlist)
    percent=percenum*100
    print(str(round(percent,2))+'%')

driver.quit()
for key,value in sepdict.items():
    nl='\\n'
    if(type(value) is list):
        outfile.write(str('"'+key+'" = "'+nl.join(value)+'";'))
        outfile.write("\n")
    else:
        outfile.write(str('"'+key+'" = "'+value+'";'))
        outfile.write("\n")
        
outfile.close()
stop=timeit.default_timer()
print('Time: '+str(round((stop-start)/60,1)) +' min')








