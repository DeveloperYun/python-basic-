from tkinter import *
from tkinter import messagebox
import sqlite3

# data 삽입 함수
def insertData():
    con, cur = None, None
    data1, data2, data3, data4 = "","","",""
    sql = ""

    con = sqlite3.connect("C:/PythonDB/naverDB")
    cur = con.cursor()

    # 엔트리로부터 값 가져옴
    data1 = edit1.get()
    data2 = edit2.get()
    data3 = edit3.get()
    data4 = edit4.get()

    try:
        # sql = "insert into userTable values('" + data1 + "','" + data1 + "','" + data1 + "'," + data4 + ")"
        # cur.execute(sql)
        cur.execute("insert into userTable(id, userName, email, birthYear) values(?,?,?,?)",\
                    (data1,data2,data3,data4))
    except:
        messagebox.showerror("error","error erupted by data insertion")
    else:
        messagebox.showinfo("success","success data insertion")
    con.commit()
    con.close()

# data 조회 함수
def selectData():
    strData1, strData2, strData3, strData4 = [],[],[],[]
    con = sqlite3.connect("C:/PythonDB/naverDB")
    cur = con.cursor()

    # 출생 연도 기준 오름차순 출력 (내림차순은 뒤에 desc 만 붙이면 된다)
    cur.execute("select * from userTable order by birthYear")

    strData1.append("userID")
    strData2.append("userName")
    strData3.append("email")
    strData4.append("birthYear")

    strData1.append("--------")
    strData2.append("--------")
    strData3.append("--------")
    strData4.append("--------")

    while True:
        row = cur.fetchone()
        if row == None:
            break
        strData1.append(row[0])
        strData2.append(row[1])
        strData3.append(row[2])
        strData4.append(row[3])
    
    # 리스트 박스를 비워줘야 꺠끗하게 출력이 된다.
    listData1.delete(0, listData1.size()-1)
    listData2.delete(0, listData2.size()-1)
    listData3.delete(0, listData3.size()-1)
    listData4.delete(0, listData4.size()-1)

    # zip을 통해 시퀀스 객체(리스트) 들을 맵핑한다.
    for item1, item2, item3, item4 in zip(strData1,strData2,strData3,strData4):
        listData1.insert(END, item1)
        listData2.insert(END, item2)
        listData3.insert(END, item3)
        listData4.insert(END, item4)
    con.close()

def DeleteData():
    con, cur = None, None
    del_id = ""
    sql = ""

    con = sqlite3.connect("C:/PythonDB/naverDB")
    cur = con.cursor()

    del_id = edit5.get()

    try:
        cur.execute("delete from userTable where id = ?",(del_id,))
    except:
        messagebox.showerror("error","error erupted by data delete")
    else:
        messagebox.showinfo("success","success data delete")

    con.commit()
    con.close()

if __name__=="__main__":
    window = Tk()
    window.geometry("800x400")
    window.title("GUI data insert")

    con = sqlite3.connect("C:/PythonDB/naverDB")
    cur = con.cursor()

    cur.execute("drop table if exists userTable")
    cur.execute("create table if not exists userTable(id char(4) primary key, userName char(15), "
            "email char(15), birthYear int)")

    editFrame = Frame(window)
    editFrame.pack()

    # 조회 결과를 출력할 프레임 컨테이너
    listFrame = Frame(window)
    # 할당된 공간을 양쪽으로 다 채우기 위해 fill=BOTH
    # expand = True(1) 미사용 공간을 현재 위젯의 할당된 공간으로 변경한다.
    listFrame.pack(side = BOTTOM, fill=BOTH, expand=1)

    edit1 = Entry(editFrame, width=10)
    edit1.pack(side = LEFT, padx = 10, pady = 10)
    edit2 = Entry(editFrame, width=10)
    edit2.pack(side = LEFT, padx = 10, pady = 10)
    edit3 = Entry(editFrame, width=10)
    edit3.pack(side = LEFT, padx = 10, pady = 10)
    edit4 = Entry(editFrame, width=10)
    edit4.pack(side = LEFT, padx = 10, pady = 10)

    #삭제를 원하는 id를 입력받기 위한 엔트리
    textentry = StringVar()
    textentry.set("삭제할 id")
    edit5 = Entry(editFrame,textvariable=textentry ,width=10)
    edit5.pack(side = LEFT, padx = 10, pady = 10)


    btnInsert = Button(editFrame, text="입력", command=insertData)
    btnInsert.pack(side=LEFT, padx=10, pady=10)
    btnSelect = Button(editFrame, text="조회", command = selectData)
    btnSelect.pack(side=LEFT, padx=10, pady=10)
    btnDelete = Button(editFrame, text="삭제", command = DeleteData)
    btnDelete.pack(side=LEFT, padx=10, pady=10)

    listData1 = Listbox(listFrame, bg="yellow")
    listData1.pack(side=LEFT, fill=BOTH, expand=1)
    listData2 = Listbox(listFrame, bg="yellow")
    listData2.pack(side=LEFT, fill=BOTH, expand=1)
    listData3 = Listbox(listFrame, bg="yellow")
    listData3.pack(side=LEFT, fill=BOTH, expand=1)
    listData4 = Listbox(listFrame, bg="yellow")
    listData4.pack(side=LEFT, fill=BOTH, expand=1)

    con.commit()
    con.close()

    window.mainloop()