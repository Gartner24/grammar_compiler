import turtle
t = turtle.Turtle()
def dibujarFlor(petalos, tamano):
    for _ in range(petalos):
        for _ in range(36):
            t.forward((tamano / 36))
            t.left(10)
        t.left((360 / petalos))
def espiralDeFlores(tamanoInicial):
    for tamano, angulo in zip(range(tamanoInicial, (tamanoInicial + 90), 15), range(0, 360, 45)):
        dibujarFlor(6, tamano)
        t.left(angulo)
espiralDeFlores(100)
turtle.mainloop()
