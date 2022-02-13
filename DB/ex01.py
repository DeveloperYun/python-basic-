import sqlite3

con, cur = None, None
pCode, pName, price, amount = "","","",""

con = sqlite3.connect("c:/PythonDB/naverDB") # db연결
cur = con.cursor()

cur.execute("drop table if exists productTable")
cur.execute("create table productTable(pCode char(5), pName char(20), price int, amount int)")

for _ in range(3):
    pCode = input("code >> ")
    pName = input("name >> ")
    price = input("price >> ")
    amount = input("amount >> ")

    cur.execute("insert into productTable(pCode,pName,price,amount) values(?, ?, ?, ?)",(pCode,pName,price,amount))

con.commit()
cur.execute("select * from productTable")
print("%5s %10s %5s %5s"%("제품코드","제품명","가격(만)","재고수량"))
print("-----------------------------------------------------------")
while True:
    row = cur.fetchone()
    if row == None:
        break
    pCode = row[0]
    pName = row[1]
    price = row[2]
    amount = row[3]

    print("%5s %20s %5d %5d"%(pCode,pName,price,amount))

con.close()