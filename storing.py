import os
from main import *
lastelement=False
count=0

if os.path.exists('storage.json'): #delete file if it alredy exists so its blank
    os.remove('storage.json')
StorageFile = open('storage.json','x')#create file
StorageFile = open('storage.json','a')#opens file for appending

InputString=myBook
StorageList=[]
word=str('')
for i in InputString:
    if count==len(InputString)-1:
        lastelement=True
    if lastelement==True:
        word+=i
        StorageList.append(word)
        break
    if str(i)!=' ':
        word+=i
    else:
        StorageList.append(word)
        word=''
    count+=1
    


#StorageList = ['ex1','ex2','ex3','ex4'] #add the actual data later
for i in StorageList:
    StorageFile.write(i)
    StorageFile.write('\n')