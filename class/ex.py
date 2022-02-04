from abc import *  # abc = abstract base class의 약자.

class Unit(metaclass = ABCMeta):
    x , y = 0 , 0
    name = ""

    # 모든 유닛들은 움직임이 다르기 때문에 추상메소드를 정의
    @abstractmethod
    def move(self, x, y):
        pass

    def stop(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
        print("now position : ",self.x, ",",self.y,"에",self.name,"이 정지")

class Tank(Unit):
    mode = ""

    # 오버라이딩
    def move(self, x, y):
        self.x = x
        self.y = y
        print("tank pos : ", self.x, ",",self.y, "로 이동")

    # 탱크 클래스의 고유 메소드
    def siegeMode(self):
        self.mode = "mode : siegemode"
        print(self.mode)

class Dropship(Unit):
    mode = ""

    # 오버라이딩
    def move(self, x, y):
        self.x = x
        self.y = y
        print("dropship pos : ", self.x, ",",self.y, "로 이동")

    # 드랍쉽 고유 메소드(수송기능)
    def load(self):
        self.mode = "mode : load"
        print(self.mode)
    
    def unload(self):
        self.mode = "mode : unload"
        print(self.mode)

class Marine(Unit):
    mode = ""

    # 오버라이딩
    def move(self, x, y):
        self.x = x
        self.y = y
        print("marine pos : ", self.x, ",",self.y, "로 이동")

    # 마린 고유 메소드
    def stimpack(self):
        self.mode = "mode : stimpack"
        print(self.mode)

tank = Tank()
tank.move(100,300)
tank.siegeMode()
tank.stop("tank1",300,400)

print("")
m1 = Marine()
m1.move(200,300)
m1.stimpack()
m1.stop("marine1",300,400)

print("")
d1 = Dropship()
d1.move(300,400)
d1.load()
d1.stop("d1",400,500)
d1.unload()