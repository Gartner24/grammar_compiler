import turtle
t = turtle.Turtle()
def drawRectangle(width, height):
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
def drawTriangle(base):
    for _ in range(3):
        t.forward(base)
        t.left(120)
def drawHouse(size):
    drawRectangle(size, (size / 2))
    drawTriangle(size)
drawHouse(300)
turtle.mainloop()
