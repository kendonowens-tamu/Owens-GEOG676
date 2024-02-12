import re
class Shape:
    def __init__(self, constructor):
        self.type = constructor[0]
        self.dim = [int(constructor[1]),int(constructor[2])]
    def getArea(self): 
        pass
    def getShape(self):
        return self.type
    def getDims(self):
        return self.dim
class Rectangle(Shape):
    def __init__(self, constructor):
        self.dim = [int(constructor[1]),int(constructor[2])]
        self.type = constructor[0]
    def getArea(self):
        return self.dim[0]*self.dim[1]
class Circle(Shape):
    def __init__(self, constructor):
        self.dim = float(constructor[1])
        self.type = constructor[0]
    def getArea(self):
        return 3.14*self.dim**2
class Triangle(Shape):
    def __init__(self, constructor):
        self.dim = [int(constructor[1]),int(constructor[2])]
        self.type = constructor[0]
    def getArea(self):
        return 0.5*(self.dim[0]*self.dim[1])



file = open("C:/Users/kendo/Documents/ArcPy/Data/shapes.csv", "r")
data = file.readlines()
file.close()
dataList = []
for x in data:
    line = re.sub(r"\n", "", x)
    dataList.append(re.split(",",line))
ShapesList = []
for x in dataList:
    if x[0] == "Rectangle":
        ShapesList.append(Rectangle(x))
    if x[0] == "Triangle":
        ShapesList.append(Triangle(x))
    if x[0] == "Circle":
        ShapesList.append(Circle(x))
count = 1
for x in ShapesList:
    print("Object number "+str(count)+" is a "+x.getShape()+" with an area of "+str(x.getArea())+" and dimensions of "+str(int(x.getDims())))
    count+=1

