import cv2
import numpy as np
import mysql.connector
from tkinter import *
import datetime
import os

import csv
fN=0
userid=0
mydb=mysql.connector.connect(host="localhost",user="root",password="",database="python")
mycursor=mydb.cursor()
def save_info():
    firstname_info=firstname.get()
    id_info=id.get()
    global fN
    fN=firstname.get()
    global userid
    userid=id.get()
    age_info=age.get()
    print(firstname_info,id_info,age_info)
    sqlFormula="INSERT INTO user (id,name,age,vote) VALUES (%s,%s,%s,%s)"
    user=(id_info,firstname_info,age_info,"")

    mycursor.execute(sqlFormula,user)
    mydb.commit()
    
    kk()

       
    
    

screen= Tk()
screen.geometry("500x500")
screen.title("User Registeration Form")
heading=Label(text="User Registeration Form",bg="grey",fg="black",width="500",height="3")

heading.pack()

firstname_text = Label(text="Name *",)
id_text = Label(text="ID * ",)
age_text = Label(text="Age * ",)
firstname_text.place(x=10,y=70)
id_text.place(x=10,y=140)
age_text.place(x=10,y=210)


firstname=StringVar()
id=IntVar()
age=IntVar()

firstname_entry = Entry(textvariable = firstname,width="30")
id_entry = Entry(textvariable = id,width="30")
age_entry = Entry(textvariable = age,width="30")

firstname_entry.place(x=15,y=100)
id_entry.place(x=15,y=170)
age_entry.place(x=15,y=240)

register= Button(screen,text = "Register",width="20",height="2",command=save_info,bg="grey")
register.place(x=15,y=290)
def run():
    
    register1= Button(screen,text = "train",width="20",height="2",command=train,bg="grey")
    register1.place(x=300,y=290)
    
    register1= Button(screen,text = "detect",width="20",height="2",command=detect,bg="grey")
    register1.place(x=160,y=360)


def train():
    os.system('trainer.py')

def detect():
    os.system('detector.py')


def kk():
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    cam=cv2.VideoCapture(0)
    print(cam.isOpened())

   # id=input('enter user id')
    sampleNum=0
    while(cam.isOpened()):
        ret,img=cam.read()
        font=cv2.FONT_HERSHEY_COMPLEX_SMALL
        sN=str(sampleNum)
        name=str(fN)
        date=str(datetime.datetime.now())
        img=cv2.putText(img,sN,(550,20),font,1,(0,255,0),2,cv2.LINE_8)
        img=cv2.putText(img,date,(10,20),font,1,(255,0,0),2,cv2.LINE_8)
        img=cv2.putText(img,name,(550,470),font,1,(0,0,255),2,cv2.LINE_8)
        #print(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        #print(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            
            sampleNum=sampleNum+1
            #print(sampleNum)
            cv2.imwrite("dataSet/User."+ str(userid)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+y,y+h),(0,255,0),2)
            
        cv2.imshow("Face",img)
        k=cv2.waitKey(1)& 0xFF
        if  k==27:
            break
        elif cv2.waitKey(1) & (sampleNum>500):
            break
            
    cam.release()
    cv2.destroyAllWindows()
    run()

