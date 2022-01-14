import turtle

## turtle graphics 라이브러리로 간단한 그림을 그릴 수 있다.
t = turtle.Pen()

## 캔버스의 마우스 형태의 그림을 거북이 모양으로 바꿔준다.
t.shape("turtle")
t.pencolor("blue")

## 직선으로 100픽셀 만큼 선을 그린다
t.forward(100)

## 오른쪽 방향으로 90도로 바꾼다.
t.right(90)
t.forward(100)

input("press any key to exit ...")