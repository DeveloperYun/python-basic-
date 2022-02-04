from cProfile import label
from distutils import command
from tkinter import *
from tkinter.filedialog import *
import os # 파일이름을 가져오기 위해 import

#---------------------------------------file menu---------------------------------
# 새파일 클릭시 호출되는 함수
def newFile():
    window.title("제목없음-메모장")
    ta.delete(1.0, END) # 새파일은 텍스트 위젯 안의 내용을 다 지우면 되므로, text의 인덱스는 
                        # (y,x) 다시 말해서 x 열을 사용한다.
                        # 1.0 이라는 것은 첫번째 줄, 첫번째 문자를 의미하게 되므로 여기서부터 삭제.

# 열기 클릭시 호출되는 함수
def openFile():
    file = askopenfilename(title="파일 열기", \
                           filetypes=(("텍스트파일","*.txt"),("모든파일","*.*")))
    # open한 파일의 이름으로 타이틀 설정
    window.title(os.path.basename(file) + "-메모장") # 이름만 가져오게 하는 os의 메소드
    ta.delete(1.0, END) # 기존의 내용을 싹다 지워야 open file의 내용을 가져올 수 있다.
    f = open(file, "r")

    # read() 는 파일 내용을 전부 문자열로 리턴해준다.
    ta.insert(1.0, f.read())
    f.close()

# 저장 클릭시 호출되는 함수
def saveFile():
    f = asksaveasfile(mode="w", defaultextension=".txt")
    
    if f is None: #file 이 없다면(빈파일은 저장할 필요x)
        return
    
    # 저장하기 위해 text widget의 내용을 처음부터 끝까지 가져오는 코드
    ts = str(ta.get(1.0, END))
    f.write(ts) # file 저장
    f.close()

# 종료 클릭시 호출되는 함수
def exit_memo():
    window.quit()
    window.destroy()
#---------------------------------------------------------------------------------

#---------------------------------------edit menu---------------------------------
# 전역변수 초기화
es = ""

# 잘라내기 클릭시 호출되는 함수
def cut():
    global es
    es = ta.get(SEL_FIRST, SEL_LAST) # es 변수에게는 "선택된 문자열을 저장한 후 삭제"
                                     # 문자열의 인덱스는 시작이 SEL_FIRST 끝이 SEL_LAST 로 접근 가능.
                                     # 선택된 문자열 부분은 색상을 주고 구분토록 한다.
    
    ta.delete(SEL_FIRST, SEL_LAST) # cut 한 부분 지우는 부분

# 복사 클릭시 호출되는 함수
def copy():
    global es
    es = ta.get(SEL_FIRST, SEL_LAST)

# 붙여넣기 클릭시 호출되는 함수
def paste():
    global es
    ta.insert(INSERT, es) # INSERT 상수는 커서의 현재 위치를 저장

def delete():
    ta.delete(SEL_FIRST,SEL_LAST)
#---------------------------------------------------------------------------------


#---------------------------------------help menu---------------------------------

def help():
    he = Toplevel(window) # 최상위 윈도우
    he.geometry("200x200")
    he.title("info")
    
    lbl = Label(he, text="python memo ver1.0")
    lbl.pack()

#---------------------------------------------------------------------------------


window = Tk()
window.title("memo")
window.geometry("400x400")

# 메모장에는 text 가 필요
ta = Text(window) # text widget

# 메모장에는 스크롤 바가 필요
sb = Scrollbar(ta)
sb.config(command=ta.yview()) # 스크롤바를 수직으로 만드는 yview
sb.pack(side=RIGHT, fill="both")

# 메모장은 자동으로 사이즈가 조절될 수 있음.
# 메모장 기본 사이즈를 400x400 으로 설정했지만, 필요에 따라 확대할 수 있어야 함.

# weight 는 상대적인 크기를 의미. 1로 설정하면 전체화면 크기에 자동으로 맞춰서 확장.
window.grid_rowconfigure(0, weight=1) # 행을 전체 사이즈로 설정함
window.grid_columnconfigure(0, weight=1) # 열을 전체 사이즈로 설정함

ta.grid(sticky=N+E+S+W) # text widget이 상하좌우를 꽉 채우도록 고정.

#---------------------menuvar-------------------------

mainMenu = Menu(window)

#filemenu 생성
fileMenu = Menu(mainMenu, tearoff=False)
mainMenu.add_cascade(label="file",menu=fileMenu)
fileMenu.add_command(label = "새파일", command=newFile)
fileMenu.add_separator()
fileMenu.add_command(label = "열기", command=openFile)
fileMenu.add_separator()
fileMenu.add_command(label = "저장", command=saveFile)
fileMenu.add_separator()
fileMenu.add_command(label = "종료", command=exit_memo)
window.config(menu=mainMenu)

# edit 생성
edit = Menu(mainMenu, tearoff=False)
mainMenu.add_cascade(label="edit", menu=edit)
edit.add_command(label="잘라내기", command=cut)
edit.add_separator()
edit.add_command(label="복사", command=copy)
edit.add_separator()
edit.add_command(label="붙여넣기", command=paste)
edit.add_separator()
edit.add_command(label="삭제", command=delete)

# 도움말 메뉴
h = Menu(mainMenu, tearoff=False)
h.add_command(label="memo info(i)", command=help)
mainMenu.add_cascade(label="help", menu=h)


#---------------------menuvar-------------------------

window.mainloop()