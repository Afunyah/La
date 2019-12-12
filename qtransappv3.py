import re, os, timeit
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

start=timeit.default_timer()
transregex=re.compile(r'"(.*)"\s*=\s*"(.*)";',re.DOTALL)

print('Processing, this may(will) take a while...')

#Select input and output file

infilename='mainfile1.txt'
textfile = open(infilename,'r')
list1 = textfile.readlines()
textfile.close()
langcode='es'
outfile=open('NewSpanish.txt','w')

#select formatting, auto detect ************* in new version

list01=[]
list2=[x.strip() for x in list1]
# print(list1)

options = Options()
options.headless=True
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
assert options.headless
driver=webdriver.Firefox(options=options,firefox_profile=firefox_profile)
url='https://translate.google.co.uk/#view=home&op=docs&sl=en&tl='+langcode
driver.get(url)
fileinput=driver.find_element_by_class_name('tlid-file-input')

fileinput.send_keys(os.getcwd()+"\\"+infilename)  ##OS SPECIFIC / \

subut=driver.find_element_by_class_name('tlid-translate-doc-button')
subut.click()
d00=driver.find_element_by_tag_name('pre')
data=d00.text
driver.quit()

datalist=data.split('\n')
dlist01=[item.strip('\n') for item in datalist]

# print(dlist01)
d1,d2,d3,d4={},{},{},{}

for item in list2:
    if (transregex.search(item)):
        t=transregex.search(item)
        d1[t.group(1)]=t.group(2)
        # print(t.group(0)) 
    else:
        pass
        #print(item)


for item in dlist01:
    # if item == '':
    #     continue
    # else:
    #     t=transregex.search(item)
    #     d2[t.group(1)]=t.group(2)
    #     print(t.group(0))

    # t=transregex.search(item)
    if (transregex.search(item)):
        t=transregex.search(item)
        d2[t.group(1)]=t.group(2)
        # print(t.group(0)) 
    elif item == '' or item == ' ':
        continue
    elif item[-3:-1]+item[-1] == ' ".':
        t=transregex.search(item.replace(item[-3:-1]+item[-1],'.";'))
        d2[t.group(1)]=t.group(2)
        # print(t.group(0))
    else:
        # print(item)
        pass
            

for k,v in d2.items():
    if '\\ n' in v:
        d3[k]=v.replace('\\ n','\\n')
    elif '\\ N' in v:
        d3[k]=v.replace('\\ N','\\n')
    else:
        d3[k]=v

for (k,v) in zip(d1,d3):
    d4[k]=d3[v]


print(len(list1))
print(len(dlist01))
print(len(list2))

print(len(d1))
print(len(d2))
print(len(d3))
print(len(d4))


for key,value in d4.items():
    outfile.write(str('"'+key+'" = "'+value+'";'))
    outfile.write("\n")
        
outfile.close()

print('DONE')
stop=timeit.default_timer()
print('Time: '+str(round((stop-start)/60,1)) +' min')