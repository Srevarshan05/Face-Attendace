import face_recognition
import cv2
import numpy as np
import os 
from datetime import datetime

path ='img'
images = []
classNames = []
myList=os.listdir(path)
print(myList)

for cl in myList:
    curImg=cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList 

def MarkAttendance(name):
    with open('attendace1.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        attname = 'present'
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now() 
            dtString=now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString},{attname}')
            
            
        
    


encodeListKnown=findEncodings(images)
print("encoding Complete")

 
#step 3 Finding Matches 

cap=cv2.VideoCapture(0)

while True:
    success,img=cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    
    facesCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,facesCurFrame)
    
    for  encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDis)
        matchIndex=np.argmin(faceDis)
        
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1=faceLoc
            y1,x2,y2,x1 =y1*4,x2*4,y2*4,x1*4

            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,x2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            
            MarkAttendance(name)
            
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)

    
