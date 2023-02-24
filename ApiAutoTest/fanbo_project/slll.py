import turtle
import math
# 创建一个turtle对象
t = turtle.Turtle()

# 设置画笔颜色和大小
# t.color('blue')
# t.pensize(1)
#
# # 设置绘图窗口的坐标系范围
# turtle.setworldcoordinates(-300, -300, 300, 300)
#
# # 绘制x轴和y轴
# t.penup()
# t.goto(-300, 0)
# t.pendown()
# t.goto(300, 0)
# t.penup()
# t.goto(0, -300)
# t.pendown()
# t.goto(0, 300)
#
# # 绘制坐标网格
# for i in range(-300, 301, 50):
#     t.penup()
#     t.goto(i, -300)
#     t.pendown()
#     t.goto(i, 300)
#     t.penup()
#     t.goto(-300, i)
#     t.pendown()
#     t.goto(300, i)




# 创建一个turtle对象

# 设置画笔颜色和大小

d = math.sqrt(3) / 3 * 120

# 计算三边长度
a = 120


# 计算半周长和面积
s = (a + a + a) / 2
area = (s * (s - a) * (s - a) * (s - a)) ** 0.5

# 计算内切圆半径和边心距
inradius = area / s
distance = inradius * 3

t.color('blue')
t.pensize(3)
t.penup()
t.goto(-60, inradius)
t.pendown()
# 绘制六芒星
pos = []
for i in range(3):
    t.forward(120)
    t.right(120)
    kkk = t.pos()
    pos.append(t.pos())
    # t.write(f'{kkk}', font=('Arial', 8, 'normal'))
t.penup()
t.goto(-20, inradius)
t.pendown()

t.left(60)
t.forward(40)
t.right(120)
t.forward(120)
t.right(120)
t.forward(120)
t.right(120)
t.forward(80)
# 定义三个顶点的坐标
x1, y1 = pos[0]
x2, y2 = pos[1]
x3, y3 = pos[2]

print(x1, y1, x2, y2, x3, y3)


# 计算重心的坐标
x_center = (x1 + x2 + x3) / 3
y_center = (y1 + y2 + y3) / 3

x, y = x_center, y_center
radius = d

# 将画笔移动到圆心
t.penup()
t.goto(x, y - radius)
t.setheading(0)
t.pendown()

# 绘制圆形
t.circle(radius)

t.penup()
t.goto(x, y - radius - 10)
t.setheading(0)
t.pendown()
t.circle(radius +10)
# t.penup()
# t.goto(d, 0)
# t.setheading(0)
# t.pendown()
# lll = t.pos()
# t.write(f"{lll}", font=('Arial', 8, 'normal'))
# print(d)
# t.circle(d)
# 隐藏turtle对象
t.hideturtle()

# 显示画布
turtle.done()
