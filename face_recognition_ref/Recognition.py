import cv2
import numpy as np
import os
from datetime import datetime
import face_recognition


class Recognition:
    """
    This class handles the face recognintion procces, the encoding for the images and comparing it to the images dataset.
    Taking attendance for the employee recognized by the camera.
    """
    def __init__(self):
        pass

    now = datetime.now()
    curr_date = now.strftime('%Y-%m-%d')

    def run(self):
        global name
        now = datetime.now()
        path = 'Images'
        images = []
        employees_names = []
        # Returns the list of names in the dicrectory path
        my_list = os.listdir(path)
        print(my_list)

        for cl in my_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            employees_names.append(os.path.splitext(cl)[0])
        print(employees_names)

        def findEncodings(images):
            """
            This method will  return the 128-dimension face encoding for each face in the image.
            input: images of the employees faces
            output: the 128 dimension face encoding in a list
                
            """
            encode_list = []
            for image in images:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(image)[0]
                encode_list.append(encode)
            return encode_list

        def mark_attendance(name):
            """
            This method will mark attendance for employees once they dedicted by the camera.
            input : The name of the employee.
            output: Write lines on the csv file with the attendance information.
            """
            def write_csv(name):
                now = datetime.now()
                day = now.strftime('%A')
                time_string = now.strftime('%H:%M:%S')
                date_string\
                    = now.strftime('%Y-%m-%d')
                today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
                if now > today8am:
                    status = 'late'
                else:
                    status = 'on time'
                f.writelines(f'\n{name},{day},{date_string},{time_string},{status}')

            with open('face_recognition_ref/attendance.csv', 'r+') as f:
                my_data_list = f.readlines()
                name_list = []
                date_list = []
                for line in my_data_list:
                    entry = line.split(',')
                    name_list.append(entry[0])
                    date_list.append(entry[2])
                    today = dict(zip(name_list, date_list))
                date_today = datetime.now().strftime('%Y-%m-%d')

                if name not in name_list:
                    write_csv(name)
                else:
                    if today[name] != date_today:
                        write_csv(name)

        encode_list_known = findEncodings(images)
        print('Encoding Complete')


        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB) # converting the image colors to make readable to recognize the face 

            faces_cur_frame = face_recognition.face_locations(img_s) # Detetciting
            encodes_cur_frame = face_recognition.face_encodings(img_s, faces_cur_frame) # return 128-dimension face encoding for the face in the image.

            for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
                matches = face_recognition.compare_faces(encode_list_known, encodeFace) # comparing the data from the images path with the list of face found
                face_dis = face_recognition.face_distance(encode_list_known, encodeFace) # The distance tells you how similar the faces are. 
                match_index = np.argmin(face_dis)
                print(match_index)

                if matches[match_index]:
                    """
                        This will draw the rectangular once the face dedicted.with the name of th employee within the box 
                    """
                    name = employees_names[match_index].title()
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    mark_attendance(name)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            cv2.imshow('Live Webcam', img)
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()

        return name

if __name__ == '__main__':
    cam = Recognition()
    cam.run()