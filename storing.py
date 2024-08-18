import os
from main import *
from PyMultiDictionary import MultiDictionary
dictionary = MultiDictionary()

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
        StorageList.append(str(word))
        break
    if str(i)!=' ':
        word+=i
    else:
        StorageList.append(str(word))
        word=''
    count+=1

#StorageList = ['ex1','ex2','ex3','ex4'] #add the actual data later
for i in StorageList:
    StorageFile.write(i)
    StorageFile.write('\n')


def getdefinition(word): #function to get the defenition of supplied variable
    word=str(word)
    print(word + ':')
    defenitionstring=str((dictionary.meaning('en',word)))
    defenitionlist=defenitionstring.split("]")
    defenitionlist.remove(defenitionlist[0])
    defenitionstring=str(defenitionlist[0])
    defenitionlist=defenitionstring.split("\'")   
        
    if str(defenitionlist[1])=='':
        print('Unknown Word')
    else:
        print(defenitionlist[1],'\n') 

