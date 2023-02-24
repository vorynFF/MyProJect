import turtle

# 设置画布大小
turtle.setup(400, 400)
turtle.bgcolor('white')

# 定义圆心坐标和半径
x, y = 0, 0
radius = 50

# 将画笔移动到圆心
turtle.penup()
turtle.goto(x, y - radius)
turtle.setheading(0)
turtle.pendown()

# 绘制圆形
turtle.circle(radius)

# 等待用户关闭窗口
turtle.done()
