import os
if os.path.exists('storage.txt'): #delete file if it alredy exists so its blank
    os.remove('storage.txt')
myfile = open('storage.txt','x')#create file
myfile = open('storage.txt','a')#opens file for appending

mylist = ['ex1','ex2','ex3','ex4'] #add the actual data later
for i in mylist:
    myfile.write(i)
    myfile.write('\n')
    #pass
