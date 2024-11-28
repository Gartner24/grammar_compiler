import turtle
t = turtle.Turtle()
def dibujarEstrella(lado, puntas):
    for _ in range(puntas):
        t.forward(lado)
        t.left((180 - (180 / puntas)))
dibujarEstrella(300, 7)
turtle.mainloop()
