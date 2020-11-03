# coding=UTF-8
import requests
import json
import simplejson
import base64
import tkinter
import tkinter.filedialog


def find_face(img_url):
    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {"api_key": 'w1dCuSyxycpc9W88J1ZTN6nHYLG1CkoU',
            "api_secret": '0vnq6zJb8VDR6p1Mc0gKssGnS4VD2xzM',
            "img_url": img_url,
            "return_landmark": 1
    }
    files = {"image_file": open(img_url, 'rb')}
    answer = requests.post(url, data=data, files=files)
    req_con = answer.content.decode("utf-8")
    req_dict = json.JSONDecoder().decode(req_con)
    req_json = simplejson.dumps(req_dict)
    req_json2 = simplejson.loads(req_json)
    faces = req_json2['faces']
    list0 = faces[0]
    rectangle = list0['face_rectangle']
    return rectangle


def merge_face(img1_url, img2_url, img_afterurl, number):
    fa1 = find_face(str(img1_url))
    fa2 = find_face(str(img2_url))
    rec1 = str(str(fa1['top'])+','+str(fa1['left'])+','+str(fa1['width'])+','+str(fa1['height']))
    rec2 = str(str(fa2['top'])+','+str(fa2['left'])+','+str(fa2['width'])+','+str(fa2['height']))
    merge_url = 'https://api-cn.faceplusplus.com/imagepp/v1/mergeface'
    f1 = open(img1_url, 'rb')
    f1_b64 = base64.b64encode(f1.read())
    f1.close()
    f2 = open(img2_url, 'rb')
    f2_b64 = base64.b64encode(f2.read())
    f2.close()
    data={"api_key": 'w1dCuSyxycpc9W88J1ZTN6nHYLG1CkoU',
          "api_secret": '0vnq6zJb8VDR6p1Mc0gKssGnS4VD2xzM',
          "template_base64": f1_b64,
          "template_rectangle": rec1,
          "merge_base64": f2_b64,
          "merge_rectangle": rec2,
          "merge_rate": number
    }
    answer = requests.post(merge_url, data=data)
    req_con = answer.content.decode("utf-8")
    req_dict = json.JSONDecoder().decode(req_con)
    result = req_dict['result']
    afterimg = base64.b64decode(result)
    file = open(str(img_afterurl), 'wb')
    file.write(afterimg)
    file.close()


window = tkinter.Tk()
window.title('来换个脸吧')

background_image = tkinter.PhotoImage(file='/Users/yiwenwong/Desktop/back.gif')
w = background_image.width()
h = background_image.height()
window.geometry('%dx%d+50+60' % (w, h))
var = tkinter.StringVar()
var.set("这是一个换脸小程序，请输入照片的目录")
background_label = tkinter.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
l = tkinter.Label(window, textvariable=var, bg='green', fg='white',  compound=tkinter.CENTER,
                  font=('Arial', 18), width=56,  height=1).grid(row=0, columnspan=5, sticky=tkinter.E+tkinter.W)
label = tkinter.Label(window, text="被换的脸", bg='green', fg='white', relief="ridge", font=('Arial', 18)).grid(row=2, column=0)
label2 = tkinter.Label(window, text="要换的脸", bg='green', fg='white', relief="ridge", font=('Arial', 18)).grid(row=4, column=0)
label3 = tkinter.Label(window, text="生成图片", bg='green', fg='white', relief="ridge", font=('Arial', 18)).grid(row=6, column=0)


def on_hit1():
    global ff1
    ff1 = tkinter.filedialog.askopenfilename()


e1 = tkinter.Button(window, text='选择文件', font=('Arial', 12),
                    width=10, height=1,
                    command=on_hit1).grid(row=2, column=3)


def on_hit2():
    global ff2
    ff2 = tkinter.filedialog.askopenfilename()


e2 = tkinter.Button(window, text='选择文件', font=('Arial', 12),
                    width=10, height=1, bg='green',
                    command=on_hit2).grid(row=4, column=3)


def on_hit3():
    global ff3
    ff3 = tkinter.filedialog.asksaveasfilename()


e3 = tkinter.Button(window, text='选择文件夹和文件名', font=('Arial', 12),
                    width=20, height=1, bg='green',
                    command=on_hit3).grid(row=6, column=3)


def on_hit():
    merge_face(ff1, ff2, ff3, 100)


m = tkinter.Button(window, text='生成', font=('Arial', 12),
                   width=10, height=1,
                   command=on_hit).grid(row=7, column=4)
window.mainloop()


