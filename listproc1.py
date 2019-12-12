import re
import shelve
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

transregex=re.compile(r'"(.*)"\s*=\s*"(.*)";',re.DOTALL)

print('Processing, this may(will) take a while...')

textfile = open('mainfile1.txt')
list1 = textfile.readlines()
kvdict = {}
#print(list1)
langcode='it'
outfile=open('Italiantrans.txt','w')

while '\n' in list1:
    list1.remove('\n')
list2=[x.strip() for x in list1]
#print(list2)

for item in list2:
    total=transregex.search(item)
    kvdict[total.group(1)]=total.group(2)
#print(kvdict)

for key,value in kvdict.items():
    #print(key+" : "+value)
    pass

translistkeys =[]
for key in kvdict.keys():
    translistkeys.append(key)
#print(translistkeys)
translistvals =[]
for val in kvdict.values():
    translistvals.append(val)
#print(translistvals)

newvals=[]
for item in translistvals:
    if '\\n' in item:
        #print(item)
        item=item.split('\\n')
    newvals.append(item)
#print(newvals)

#print(len(translistkeys),len(newvals))
sepdict={}
for (k,v) in zip(translistkeys,newvals):
    sepdict[k] = v
#print(sepdict)

'''
options = Options()
options.set_headless()
assert options.headless
driver=webdriver.Firefox(firefox_options=options)
driver.quit()'''

newrefvals=[]
itemlist=list(sepdict.items())
for key,value in sepdict.items():
    #print(type(value))
    x=False
    if(type(value) is list):
        tempvals=[]
        for item in value:
            sval=str(item).split(" ")
            sepval='%20'.join(sval)
            #print(sepval)
            options = Options()
            options.set_headless()
            firefox_profile = webdriver.FirefoxProfile()
            firefox_profile.set_preference('permissions.default.image', 2)
            firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
            assert options.headless
            driver=webdriver.Firefox(firefox_options=options,firefox_profile=firefox_profile)
            driver.get("https://translate.google.co.uk/#en/"+langcode+"/"+sepval)
            resultz=driver.find_elements_by_css_selector('#result_box>span')
            #print(resultz[0].text)
            if len(resultz)!= 0:
                tran=resultz[0].text
                #print(tran)
                tempvals.append(tran)
                x=True
            else:
                #x=False
                driver.quit()
                options = Options()
                options.set_headless()
                firefox_profile = webdriver.FirefoxProfile()
                firefox_profile.set_preference('permissions.default.image', 2)
                firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
                assert options.headless
                driver=webdriver.Firefox(firefox_options=options,firefox_profile=firefox_profile)
                driver.get("https://translate.google.co.uk/#en/"+langcode+"/"+sepval)
                resultz=driver.find_elements_by_css_selector('#result_box>span')
                #print(resultz[0].text)
                if len(resultz)!= 0:
                    tran=resultz[0].text
                    #print(tran)
                    tempvals.append(tran)
                    x=True
                else:
                    x=False
            driver.quit()
        if x:
            newstr="\\n".join(tempvals)
            #newrefvals.append(newstr)
            sepdict[key]=newstr
            '''if newstr in sepdict[key]:
                print("Processed >> "+key+" : "+sepdict[key])'''
        else:
            print("Not processed>> "+key+" : "+"\\n".join(value))

        
        '''
        sval1=str(value[0]).split(" ")
        sval2=str(value[1]).split(" ")
        sepval1='%20'.join(sval1)
        sepval2='%20'.join(sval2)
        #print(sepval1+" : "+sepval2)
        driver.get("https://translate.google.co.uk/#en/de/"+)
        '''
    else:
        pass
        rval=str(value).split(" ")
        refval='%20'.join(rval)
        #print(refval)
        #print(type(refval))
        options = Options()
        options.set_headless()
        assert options.headless
        driver=webdriver.Firefox(firefox_options=options)
        driver.get("https://translate.google.co.uk/#en/"+langcode+"/"+refval)
        resultz=driver.find_elements_by_css_selector('#result_box>span')
        #print(resultz[0].text)
        if len(resultz)!= 0:
            tran=resultz[0].text
            #print(tran)
            sepdict[key]=tran
        else:
            driver.quit()
            options = Options()
            options.set_headless()
            assert options.headless
            driver=webdriver.Firefox(firefox_options=options)
            driver.get("https://translate.google.co.uk/#en/"+langcode+"/"+refval)
            resultz=driver.find_elements_by_css_selector('#result_box>span')
            #print(resultz[0].text)
            if len(resultz)!= 0:
                tran=resultz[0].text
                #print(tran)
                sepdict[key]=tran
            else:
                print("Not processed>> "+key+" : "+value)
        driver.quit()

    num=itemlist.index((key,value))
    percenum=num/len(itemlist)
    percent=percenum*100
    print(str(round(percent,2))+'%')

shelfile=shelve.open('transdata')
shelfile['transdict']=sepdict
shelfile.close
#print(sepdict)

for key,value in sepdict.items():
    nl='\\n'
    if(type(value) is list):
        outfile.write(str('"'+key+'" = "'+nl.join(value)+'";'))
        outfile.write("\n")
    else:
        outfile.write(str('"'+key+'" = "'+value+'";'))
        outfile.write("\n")
        
outfile.close()






