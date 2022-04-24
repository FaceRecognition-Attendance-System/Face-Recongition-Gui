import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd
# from PIL import ImageGrab
class Recognition:
    def __int__(self):
        pass

    def run(self):
        path='Images'
        images = []
        EmployeesNames = []
        myList = os.listdir(path)
        print(myList)
        now = datetime.now()
        curr_date = now.strftime('%Y-%m-%d')


        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            EmployeesNames.append(os.path.splitext(cl)[0])
        print(EmployeesNames)

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def markAttendance(name):
            with open('Attendance.csv', 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                datelist = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                    datelist.append(entry[2])
                    today = dict(zip(nameList, datelist))
                now = datetime.now().strftime('%Y-%m-%d')

                # can use a function instead of repeating the same code below
                if name not in nameList:
                    now = datetime.now()
                    day= now.strftime('%A')
                    timeString = now.strftime('%H:%M:%S')
                    dateString = now.strftime('%Y-%m-%d')
                    today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
                    if now > today8am:
                        status = 'late'
                    else:
                        status = 'on time'
                    f.writelines(f'{name},{day},{dateString},{timeString},{status}\n')

                else:
                    if today[name] != now:
                        now = datetime.now()
                        day = now.strftime('%A')
                        timeString = now.strftime('%H:%M:%S')
                        dateString = now.strftime('%Y-%m-%d')
                        today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
                        if now > today8am:
                            status = 'late'
                        else:
                            status = 'on time'
                        f.writelines(f'{name},{day},{dateString},{timeString},{status}\n')



                # if name not in nameList or curr_date not in datelist:
                #     now = datetime.now()
                #     day= now.strftime('%A')
                #     timeString = now.strftime('%H:%M:%S')
                #     dateString = now.strftime('%Y-%m-%d')
                #     today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
                #     if now > today8am:
                #         status = 'late'
                #     else:
                #         status = 'on time'
                #     f.writelines(f'{name},{day},{dateString},{timeString},{status}\n')

            # df = pd.read_csv("Attendance.csv")
            # Name_list = df["Name"].tolist()
            # for name in Name_list:
            #     names = df[df['Name'] == name]
            # now = datetime.now()
            # dateString = now.strftime('%Y-%m-%d')
            # today = df[df['Date'] == dateString]
            # today.to_csv('Today_Attendance.csv',index=False)


        encodeListKnown = findEncodings(images)
        print('Encoding Complete')

        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)
                print(matchIndex)

                if matches[matchIndex]:
                    name = EmployeesNames[matchIndex].title()
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            cv2.imshow('Live Webcam', img)
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    cam=Recognition()
    cam.run()