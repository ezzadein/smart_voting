import cv2
import numpy as np
from tkinter import *
import os

import mysql.connector



global i_d
mydb=mysql.connector.connect(host="localhost",user="root",password="",database="python")
print(mydb)
screen= Tk()


def check():
    got=0
    mycursor=mydb.cursor()
    sqlFormula="SELECT * FROM user WHERE id="+str(i_d)
    mycursor.execute(sqlFormula)
    myresult=mycursor.fetchall()
    for row in myresult:
       
        if(row[4]!=""):
            got=1
    return got


def save_info():
  
    mycursor=mydb.cursor()
    sqlFormula="UPDATE user SET vote ='YSRCP' WHERE id="+str(i_d)
    print(id)
    mycursor.execute(sqlFormula)
    mydb.commit()
    screen.destroy()

def TDP_info():

    mycursor=mydb.cursor()
    sqlFormula="UPDATE user SET vote ='TDP' WHERE id="+str(i_d)
    mycursor.execute(sqlFormula)
    mydb.commit()
    screen.destroy()

def JSP_info():
  
    mycursor=mydb.cursor()
    sqlFormula="UPDATE user SET vote ='JSP' WHERE id="+str(i_d)
    print(id)
    mycursor.execute(sqlFormula)
    mydb.commit()
    screen.destroy()
    
    
    
def opentkinter():
    
    
    screen.geometry("600x500")
    screen.title("Mark Your VOte")
    heading=Label(text="Mark Your Vote",bg="grey",fg="black",width="500",height="3")

    heading.pack()


    YSRCP= Button(screen,text = "YSRCP",width="20",height="2",command=save_info,bg="grey")
    YSRCP.place(x=15,y=290)

    
    TDP= Button(screen,text = "TDP",width="20",height="2",command=TDP_info,bg="grey")
    TDP.place(x=200,y=290)

    
    JSP= Button(screen,text = "JSP",width="20",height="2",command=JSP_info,bg="grey")
    JSP.place(x=380,y=290)


    
    



faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cam=cv2.VideoCapture(0)

#recognizer= cv2.createLBPHFaceRecognizer()
rec=cv2.face.LBPHFaceRecognizer_create()
rec.read('recognizer\\trainingData.yml')
id=0
font=cv2.FONT_HERSHEY_SIMPLEX
font = cv2.FONT_HERSHEY_SIMPLEX 
  
# org 
org = (50, 50) 
  
# fontScale 
fontScale = 1
   
# Blue color in BGR 
color = (255, 0, 0) 
  
# Line thickness of 2 px 
thickness = 2

dicti={}
while(True):
    chk=1
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+y,y+h),(0,255,0),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
           
        print(conf)
        if(conf<=60.00):
            img = cv2.putText(img,str(id), (x+5,y+h), font,  
                   fontScale, color, thickness, cv2.LINE_AA)
           
            if(not bool(dicti)):
                dicti[id]=1;
            elif id in dicti:
                dicti[id]+=1
        if(bool(dicti)):
            
            if(dicti[id]>10):
                i_d=id
                print(dicti)
                chk=0
              
    if(chk==0):
        if(check()==0):
            opentkinter()
            cv2.destroyAllWindows()
            break
        
        else:
            screen3=Tk()
            screen3.geometry("500x500")
            screen3.title(" VOted")
            heading3=Label(screen3,text="alreaady voted",bg="grey",fg="black",width="500",height="3")

            heading3.pack()
            button1=Button(screen3,text="cancel",width="20",height="2",command=screen3.destroy,bg="gray",fg="blue")
            button1.place(x=180,y=260)
            #screen3.after(5000,screen3.destroy)
            print("You had already voted")
            cv2.destroyAllWindows()
            screen.destroy()
            break
            
   
            
                
            
        #img=cv2.putText(img,str(id),(x,y+h),font,255,cv2.LINE_AA)
       
        
    cv2.imshow("Face",img)
    if(cv2.waitKey(1)==ord('q')):
        break
cam.release;
