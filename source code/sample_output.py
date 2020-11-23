import os
import glob
import cv2
from tkinter import *
from tkinter import filedialog 
from PIL import ImageTk,Image  
from sklearn import metrics
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import random
# window configuration

display_window = Tk() 
display_window.geometry("650x650") 
display_window.title('IIVP Course Project') 

# path to the file (image)
filename = None

classifier = RandomForestClassifier(n_estimators=100,max_depth =4)

def load_dataset():
  total_in_this_case = 2276
  data = []
  tag = []
  for i in range(0,8,1):
    dic={}
    file_link = "E:\\all_pikles\\tastyPickle" + str(i)
    f=open(file_link, 'rb')
    dic = pickle.load(f)
    for x, y in zip(dic['data'], dic['tag']) :
      data.append(x) 
      tag.append(y)
  progress_tag.configure(text="Dataset loading completed")
  data = np.array(data)
  tag = np.array(tag)
  x_train, x_test, y_train, y_test = train_test_split(data, tag, test_size=0.2)
  len_a = x_train.shape[0]
  len_b = x_test.shape[0]
  print(len_a, len_b)
  x_train = x_train.reshape(len_a,64*64*3)
  x_test = x_test.reshape(len_b,64*64*3)
  classifier.fit(x_train, y_train)


def browseFiles(): 
    global filename
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File",) 
       
    file_chosen.configure(text="File Chosen:- " + filename, fg="purple") 

    load = Image.open(filename)
    load = load.resize((300, 200), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(x=190, y=325)
    

def extractWindow(img):
  l=[]
  rows,cols=img.shape[:2]
  windSize=64
  stride=32
  for i in range(0,rows-windSize+1,32):
    for j in range(0,cols-windSize+1,32):
      if (i+windSize)>=rows or j+windSize>=cols:
        continue
      variable = random.randint(0,40)
      arr = [2,5,7,9,11,13]
      if variable not in arr:
        continue
      subSec=[]
      count1s=0
      for u in range(windSize):
        temp=[]
        for v in range(windSize):
          r=img[i+u][j+v][0]
          g=img[i+u][j+v][1]
          b=img[i+u][j+v][2]
          temp.append((r,g,b))
        subSec.append(temp)
      l.append(subSec)
  return l

def classifyImage():
  img=cv2.imread(filename)
  all_windows = extractWindow(img)
  collect = []
  for someThing in all_windows:
    collect.append(someThing)
  dict1={'data':collect}
  f1 = open('testingPickle_1', 'ab') 
  pickle.dump(dict1, f1)                      
  f1.close()    
  dic={}
  file_link = "C:\\Users\\Dell\\Desktop\\demo\\testingPickle_1" 
  f=open(file_link, 'rb')
  dic = pickle.load(f)
  collect = []
  for x in dic['data']:
    collect.append(x)     
  collect = np.array(collect) 
  new_len = (collect.shape[0])
  collect = collect.reshape(new_len,64*64*3)
  predictions = classifier.predict(collect)
  print(predictions)
  max_chain = 0;
  count = 0;
  ones = 0
  zeros = 0
  for i in range(len(predictions)):
    if predictions[i] == 1:
      count += 1
      ones += 1
      max_chain = max(max_chain, count)
    else :
      count = 0
      zeros += 1
  max_chain = max(max_chain, count)
  if max_chain >= 4:
    file_chosen.configure(text="This image appears to be spliced", fg="red") 
  else :
    file_chosen.configure(text="This image is authentic", fg="green") 
  print(ones, zeros)

display_window.config(background = "white") 
   
welcome_tag = Label(display_window,text = "Image splicing detection", width = 100, height = 4, fg = "blue",justify="center") 
file_chosen = Label(display_window, text = "", width = 100, height = 4, fg = "blue")
open_explorer = Button(display_window, text = "Browse Files", command = browseFiles)  
button_exit = Button(display_window, text = "Exit", command = exit) 
button_process = Button(display_window,  text = "Classify Image", command = classifyImage)  
loadDataset = Button(display_window,  text = "load Dataset", command = load_dataset)  
progress_tag = Label(display_window,text = "", width = 40, height = 4, fg = "blue") 


welcome_tag.place(x=0, y=25)
file_chosen.place(x=0,y=220)
open_explorer.place(x=25, y=110)
loadDataset.place(x=25,y=170)
button_exit.place(x=600, y=600)
button_process.place(x=25,y=600)
progress_tag.place(x=250,y=120)

#load_dataset()

display_window.mainloop() 







