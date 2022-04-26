
from datetime import datetime
from face_recognition_ref.Recognition import Recognition
import cv2


def test_opencam():
    cam = cv2.VideoCapture(0)
    actual=cam.read()
    assert actual[0] == True

def test_recognition():
    recog = Recognition()
    actual= recog.run()

    expected = 'Zaid Jarrar'
    assert actual == expected

def test_recognition2():
    recog = Recognition()
    actual= recog.run()

    expected = 'Barham Farraj'
    assert actual == expected

def test_recognition3():
    recog = Recognition()
    actual = recog.run()

    expected = 'Elon'
    assert actual == expected

def test_csv_attendance_headers():
    with open('face_recognition_ref/attendance.csv') as f:
        data=f.readlines()
        actual = data[0].strip()
        expected = 'Name,Day,Date,Time,Status'
        assert actual == expected


def test_csv_attendance():
    with open('face_recognition_ref/attendance.csv') as f:
        data=f.readlines()
        actual = data[1].strip()
        expected = 'Barham Farraj,Saturday,2022-04-21,13:28:05,late'
        assert actual == expected

def test_date_changing_today():

    date_today = datetime.now().strftime('%Y-%m-%d')

    with open('face_recognition_ref/attendance.csv') as f:
        data=f.readlines()
        for i in data:

           headers = i.split(",")

        actual = headers[2]
        assert actual == date_today


def test_status():
    with open('face_recognition_ref/attendance.csv') as f:
        now = datetime.now()
        today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
        data=f.readlines()
        for i in data:
           headers = i.split(",")
        if now > today8am:
            status = 'late'
            assert headers[4] == 'late'
        else:
            status = 'on time'
            assert headers[4] == 'on time'

