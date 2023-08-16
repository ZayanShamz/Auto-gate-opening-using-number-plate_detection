import threading
import cv2
from tkinter import *
from PIL import Image, ImageTk
import pytesseract
import numpy as np
import pymysql
from flask import *

app = Flask(__name__)

con = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='anpr')
cmd = con.cursor()


data = {}
plateList = []
c = 0
temp = ''
resp = None


def refrsh():
    cmd.execute("SELECT `plate`, `name` FROM `plates`")
    for i in cmd.fetchall():
        data[i[0]] = i[1]
        plateList.append(i[0])
    print(plateList)
    print(data)


refrsh()


root = Tk()
root.title("Numberplate Recognition")
root.resizable(False, False)
root.config(bg="black")
root.geometry("650x550")
root.bind('<Escape>', lambda e: root.quit())  # Press Escape to exit

l1 = Label(root, compound="center", anchor="center", relief="raised", bg="black")
l1.pack()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
frameWidth = int(cap.get(3))
frameHeight = int(cap.get(4))
cap.set(10, 150)

# pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
tess_config = r"--psm 6 --oem 3"
plateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

minArea = 500
cancel = False
resp = "invalid"


def addVehicle():
    global cancel
    cancel = True
    l1.pack_forget()

    lName.place(bordermode="inside", relx=.3, rely=0.3, anchor="center", width=200, height=40)
    lNumber.place(bordermode="inside", relx=.3, rely=0.45, anchor="center", width=200, height=40)

    eName.place(bordermode="inside", relx=.75, rely=0.3, anchor="center", width=200, height=40)
    eNumber.place(bordermode="inside", relx=.75, rely=0.45, anchor="center", width=200, height=40)

    bSubmit.place(bordermode="inside", relx=.5, rely=0.55, anchor="center", width=100, height=40)

    bCam.place(bordermode="inside", relx=.65, rely=0.95, anchor="center", width=100, height=40)
    bClose.place(bordermode="inside", relx=.85, rely=0.95, anchor="center", width=100, height=40)


def check(frame):
    global cancel, resp, temp
    if not cancel:
        bCam.place_forget()
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)
        for (x, y, w, h) in numberPlates:
            area = w * h
            if area > minArea:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
                plate = frame[y:y + h, x:x + w]

                plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
                kernel = np.ones((1, 1), np.uint8)
                plate1 = cv2.dilate(plate_gray, kernel, iterations=1)
                plate1 = cv2.erode(plate1, kernel, iterations=1)

                value = pytesseract.image_to_string(plate1, config=tess_config)
                value = ''.join(e for e in value if e.isalnum())  # filtering
                cv2.imshow("plate", plate1)
                if value in plateList and value != temp:
                    temp = value
                    resp = "valid"
                    print("yes", data[value])


def openCam():
    global cancel, lName, lNumber, eName, eNumber, bSubmit
    cancel = False

    bClose.place(bordermode="inside", relx=.75, rely=0.95, anchor="center", width=200, height=40)
    lName.place_forget()
    lNumber.place_forget()
    bSubmit.place_forget()

    eName.place_forget()
    eNumber.place_forget()

    l1.pack()
    show_frame()


def quitFn():
    global cancel
    cancel = True
    cap.release()
    cv2.destroyAllWindows()
    l1.quit()
    root.quit()


def submit():
    name = eName.get()
    num = eNumber.get()
    num = ''.join(e for e in num if e.isalnum())
    cmd.execute("insert into plates values(null,'" + num + "', '" + name + "')")
    con.commit()
    eName.delete(0, END)
    eNumber.delete(0, END)
    refrsh()


def show_frame():
    global cancel, c
    success, frame = cap.read()

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    l1.imgtk = imgtk
    l1.configure(image=imgtk)
    c += 1
    check(frame)

    if not cancel:
        l1.after(1, show_frame)


def main():
    global cancel
    if cancel:
        cap.release()
        cv2.destroyAllWindows()
        l1.quit()
        root.quit()

    else:
        show_frame()
        threading.Thread(target=flaskRun).start()
        root.mainloop()


def flaskRun():
    app.run(host='0.0.0.0', port=5000)


lName = Label(root, text="Enter Name :", font="Helvetica, 16")
lNumber = Label(root, text="Enter Plate Number :", font="Helvetica, 16")
bSubmit = Button(root, text="ADD", font="Helvetica, 16", command=submit)

eName = Entry(root, width=200)
eNumber = Entry(root, width=200)

bClose = Button(root, text="Quit", command=quitFn)
bClose.place(bordermode="inside", relx=.75, rely=0.95, anchor="center", width=200, height=40)

# bClose = Button(root, text="Close", command=close)
# bClose.place(bordermode="inside", relx=.75, rely=0.95,anchor="center", width=200, height=40)

bCam = Button(root, text="Open Camera", command=openCam)
bCam.place(bordermode="inside", relx=.75, rely=0.95, anchor="center", width=200, height=40)

bAdd = Button(root, text="Add New Vehicle", command=addVehicle)
bAdd.place(bordermode="inside", relx=.3, rely=0.95, anchor="center", width=200, height=40)


@app.route('/test', methods=['POST', 'GET'])
def test():
    global resp
    response = 'ok'
    if resp == "valid":
        response = "valid"
        resp = None
    print(response)
    return response


if __name__ == '__main__':
    main()
    cap.release()
    cv2.destroyAllWindows()
