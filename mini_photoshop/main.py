from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import askfloat, askinteger
# pillow lib 에 필요한 것들 import
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from numpy import newaxis

window, canvas, paper = None, None, None # 작업은 paper 위에서
photo, photo2 = None, None # 원본 이미지, 포샵 이미지

originX,originY = 0, 0 # 원본 이미지 폭과 높이

def displayImage(img, width, height):
    global window,canvas,paper,photo,photo2,originX,originY
    window.geometry(str(width)+"x"+str(height))
    
    # 기존에 캔버스에 출력된 그림이 있다면
    if canvas != None:
        canvas.destroy()

    # canvas 생성
    canvas = Canvas(window, width=width, height=height)
    paper = PhotoImage(width=width,height=height)

    # 이미지 폭과 높이 절반의 값의 위치에 이미지를 생성
    canvas.create_image((width/2, height/2), image=paper)

    rgbString = ""
    rgbImage = img.convert('RGB')

    # 그림의 높이와 너비만큼 돌면서 rgb 값을 getpixel 함수로 추출하여 16진수 꼴로 
    # rgbString 에 누적시키기 위함
    for i in range(0,height):
        tmpString = ""
        for j in range(0, width):
            # 복사된 이미지 객체에 getpixel() 을 이용하여 rgb 값을 얻어낼 수 있다.
            r, g, b = rgbImage.getpixel((j, i))

            # 내부루프 한번 끝날 때, 가로에 대해서 rgb값이 쭈욱 저장된다.
            tmpString += "#%02x%02x%02x " % (r, g, b) # x값 뒤에는 한 칸 공백을 두어야한다.
        
        rgbString += "{" + tmpString + "} "
    print(rgbString)

    # 그림을 대입하는 put 메소드
    # rgb 문자열 값을 paper에 대입시켜서 이미지를 출력하기 위함.
    paper.put(rgbString)
    canvas.pack()

def func_open():
    global window,canvas,paper,photo,photo2,originX,originY
    readFp = askopenfilename(parent=window,title="파일 열기",\
                        filetypes=(("모든 그림 파일", "*.jpg;*.jpeg;*.bmp;*.png;*.tif;*.gif"),\
                                    ("모든 파일","*.*")))

    # 내장함수의 photoimage() 는 한계가 있어서 pillow lib의 Image.open() 채용.
    # 사용자가 선택한 이미지를 읽고 RGB 모드로 변환
    photo = Image.open(readFp).convert('RGB')
    originX = photo.width
    originY = photo.height

    photo2 = photo.copy() # 원본이미지 복사
    newX = photo2.width
    newY = photo2.height

    print(newX, newY)
    displayImage(photo2,newX,newY)

def func_save():
    global window,canvas,paper,photo,photo2,originX,originY

    # 복사된 객체가 없으므로 저장할 수가 없음
    if photo2 == None:
        return

    saveFp = asksaveasfile(parent=window, mode="w", defaultextension=".jpg",\
                           filetypes=(("JPG 파일","*.jpg;*.jpeg"),("모든 파일", "*.*")))
    # 사용자가 입력한 파일 명으로 저장
    photo2.save(saveFp.name)

def func_exit():
    window.quit()
    window.destroy()

def func_zoom_in():
    global window,canvas,paper,photo,photo2,originX,originY

    # user에게 숫자를 입력받는다.
    scale = askinteger("확대 배수", "몇 배로 확대할까요?(2~5)", minvalue=2, maxvalue=5)

    photo2 = photo.copy()

    # pillow lib의 resize 메소드..단 메모리/속도적으로 약간 무겁다.
    photo2 = photo2.resize((int(originX * scale),int(originY * scale)))
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_zoom_out():
    global window,canvas,paper,photo,photo2,originX,originY

    # user에게 숫자를 입력받는다.
    scale = askinteger("축소 배수", "몇 배로 축소할까요?(2~5)", minvalue=2, maxvalue=5)

    photo2 = photo.copy()

    # pillow lib의 resize 메소드..단 메모리/속도적으로 약간 무겁다.
    photo2 = photo2.resize((int(originX / scale),int(originY / scale)))
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_mirror1():
    global window,canvas,paper,photo,photo2,originX,originY

    photo2 = photo.copy()

    #image  반전 메소드 transpose
    photo2 = photo2.transpose(Image.FLIP_TOP_BOTTOM)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_mirror2():
    global window,canvas,paper,photo,photo2,originX,originY

    photo2 = photo.copy()

    #image  반전 메소드 transpose
    photo2 = photo2.transpose(Image.FLIP_LEFT_RIGHT)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_rotate():
    global window,canvas,paper,photo,photo2,originX,originY
    degree = askinteger("회전","몇 도 회전할까요?", minvalue=0, maxvalue=360)

    photo2 = photo.copy()

    # img를 회전할 떄 쓰는 rotate.
    # 매개변수 (각도, expand)...expand = True라면 회전 결과 이미지를 유동적으로 확대.
    #                          expand = False 라면 원본 사이즈 유지
    photo2 = photo2.rotate(degree, expand=True)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_bright():
    global window,canvas,paper,photo,photo2,originX,originY
    value = askfloat("밝게","얼마나 밝게 할까요?(1.0~16.0)",minvalue=1.0,maxvalue=16.0)

    photo2 = photo.copy()

    # 이미지 밝기 조절 메소드 ImageEnhance.Brightness(이미지).enhance(밝기값)
    # 밝기값 1.0 = 원본 1.0초과는 점점 밝게, 1.0미만은 점점 어둡게
    photo2 = ImageEnhance.Brightness(photo2).enhance(value)

    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_dark():
    global window,canvas,paper,photo,photo2,originX,originY
    value = askfloat("어둡게","얼마나 어둡게 할까요?(1.0~0.0)",minvalue=0.0,maxvalue=1.0)

    photo2 = photo.copy()

    # 이미지 밝기 조절 메소드 ImageEnhance.Brightness(이미지).enhance(밝기값)
    photo2 = ImageEnhance.Brightness(photo2).enhance(value)
    
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_blur():
    global window,canvas,paper,photo,photo2,originX,originY

    photo2 = photo.copy()

    # 이미지에 특수 효과를 주는 filter(ImageFilter.속성)
    # 이미지 블러를 해주는 filter 메소드의 blur
    photo2 = photo2.filter(ImageFilter.BLUR)
    
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_embo():
    global window,canvas,paper,photo,photo2,originX,originY

    photo2 = photo.copy()

    # 이미지에 특수 효과를 주는 filter(ImageFilter.속성)
    photo2 = photo2.filter(ImageFilter.EMBOSS)
    
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_be_black():
    global window,canvas,paper,photo,photo2,originX,originY

    photo2 = photo.copy()

    # 컬러를 흑백으로 바꾸려면 ImageOps.grayscale(이미지) 를 쓰면 된다.
    photo2 = ImageOps.grayscale(photo2)
    
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

if __name__=="__main__":
    window = Tk()
    window.geometry("500x500")
    window.title("미니포토샵")

    # menu바 생성
    mainMenu = Menu(window) 
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu, tearoff=False)
    mainMenu.add_cascade(label="file", menu=fileMenu)
    fileMenu.add_command(label="열기", command=func_open)
    fileMenu.add_separator()
    fileMenu.add_command(label="저장", command=func_save)
    fileMenu.add_separator()
    fileMenu.add_command(label="종료", command=func_exit)

    imageMenu1 = Menu(mainMenu, tearoff=False)
    mainMenu.add_cascade(label="이미지처리(1)",menu=imageMenu1)
    imageMenu1.add_command(label="확대",command=func_zoom_in)
    imageMenu1.add_separator()
    imageMenu1.add_command(label="축소",command=func_zoom_out)
    imageMenu1.add_separator()
    imageMenu1.add_command(label="상하 반전",command=func_mirror1)
    imageMenu1.add_separator()
    imageMenu1.add_command(label="좌우 반전",command=func_mirror2)
    imageMenu1.add_separator()
    imageMenu1.add_command(label="회전",command=func_rotate)

    imageMenu2 = Menu(mainMenu, tearoff=False)
    mainMenu.add_cascade(label="이미지처리(2)",menu=imageMenu2)
    imageMenu2.add_command(label="밝게",command=func_bright)
    imageMenu2.add_separator()
    imageMenu2.add_command(label="어둡게",command=func_dark)
    imageMenu2.add_separator()
    imageMenu2.add_command(label="블러링",command=func_blur)
    imageMenu2.add_separator()
    imageMenu2.add_command(label="엠보싱",command=func_embo)
    imageMenu2.add_separator()
    imageMenu2.add_command(label="흑백처리",command=func_be_black)

    window.mainloop()
