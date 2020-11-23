import os
import glob
import cv2
import numpy as np
from PIL import Image
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import random
import pickle 

flag =0
def extractWindowFake(img,mask):
	l=[]
	rows,cols=img.shape[:2]
	windSize=64
	stride=32
	for i in range(0,rows-windSize+1,32):
		for j in range(0,cols-windSize+1,32):
			if (i+windSize)>=rows or (j+windSize) >=cols:
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
					temp_val = 0
					try:
						temp_val = mask[i+u][j+v]
					except:
						pass
					if temp_val==255:
						count1s+=1
				subSec.append(temp)
			if count1s>1600 and (windSize**2-count1s)>1600:
				l.append(subSec)
	return l
def extractWindow(img):
	l=[]
	rows,cols=img.shape[:2]
	windSize=64
	stride=32
	for i in range(0,rows-windSize+1,32):
		for j in range(0,cols-windSize+1,32):
			if (i+windSize)>=rows or j+windSize>=cols:
				continue
			if random.randint(0,40)!=5:
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
path1="D:\\Downloads\\4cam_splc"
path2="D:\\Downloads\\4cam_auth"
path3="D:\\Downloads\\4cam_splc\\edgemask"
mylist1 = [f for f in glob.glob(os.path.join(path1,"*.tif"))]
mylist2 = [f for f in glob.glob(os.path.join(path2,"*.tif"))]
mylistMask=[f for f in glob.glob(os.path.join(path3,"*.jpg"))]


r1=range(170,180,1)	# Decrease the range by 10 to create more batches
r2=range(300,320,2) # Decrease the range by 20 to create more batches
data=[]
tag=[]
for i,j in zip(r1,r2):
	flag+=1
	img=cv2.imread(mylist1[i])
	mask=cv2.imread(mylistMask[j])
	mask=cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
	ret,mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	l=extractWindowFake(img,mask)
	for someThing in l:
		data.append(someThing)
		tag.append(1)
	'''
	cv2.imshow("org",img)
	cv2.imshow("mask",mask)
	cv2.waitKey(0)
	break
	'''
for i in r1:
	flag+=1
	img=cv2.imread(mylist2[i])
	l=extractWindow(img)
	for someThing in l:
		data.append(someThing)
		tag.append(0)

dict1={'data':data,'tag':tag}
f1 = open('tastyPickle16', 'ab') 
pickle.dump(dict1, f1)                      
f1.close()