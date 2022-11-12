from random import randrange
import turtle

# setup the screen
sc = turtle.Screen()
sc.bgcolor("black")
sc.setup(600,600)
sc.tracer(0)

# create small rectangle unit
# x_len = 60, y_len = 20
rectCors = ((10,-30),(10,30),(-10,30),(-10,-30))
sc.register_shape('small_rectangle',rectCors)

# create big rectangle unit
# x_len = 120 y_len = 20
rectCors = ((10,-60),(10,60),(-10,60),(-10,-60))
sc.register_shape('big_rectangle',rectCors)

# my square
rectCors = ((10,-10),(10,10),(-10,10),(-10,-10))
sc.register_shape('sq',rectCors)

# setup the paddle that moves
def create_main_paddle():
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("big_rectangle")
    paddle.penup()
    paddle.goto(0, -250)
    paddle.color("white")
    return paddle

# method that create a paddle (to hit)
def create_target(x_center_coordinates, y_center_coordinates, is_small):
    t = turtle.Turtle()
    if(is_small == True):
        t.shape('small_rectangle')
    else:
        t.shape('big_rectangle')
    t.speed(0)
    t.penup()
    t.goto(x_center_coordinates, y_center_coordinates)
    t.color("red")
    
    return t

# method to create all paddles (to hit)
def position_targets():
    
    arrTurtles = []
    
    # big ones
    arrTurtles.append(create_target(0,250,False))
    arrTurtles.append(create_target(-200,250,False))
    arrTurtles.append(create_target(200,250,False))
    # small ones
    arrTurtles.append(create_target(0,200,True))
    arrTurtles.append(create_target(-200,200,True))
    arrTurtles.append(create_target(200,200,True))
    
    return arrTurtles

# method that creates the ball
def create_ball():
    t = turtle.Turtle()
    t.speed(0)
    t.shape("sq")
    t.penup()
    t.goto(0, 0)
    t.color("green")
    return t


p = create_main_paddle()
array_targets = position_targets()
array_targets.append(p)
b = create_ball()



# movements
def paddle_right():
    if p.xcor() < 240:
        p.setx(p.xcor() + 15)
def paddle_left():
    if p.xcor() > -240:
        p.setx(p.xcor() - 15)
        

# Keyboard bindings
sc.listen()
sc.onkeypress(paddle_right, "Right")
sc.onkeypress(paddle_left, "Left")
 
x_movement = 0.06 * randrange(-5,-1)
y_movement = 0.06 * randrange(-5,-1)

# main execution
while True:
    finished = False
    # ball hitting right and left walls
    if b.xcor() >= 290 or b.xcor() <= -290:
        x_movement = (-1* x_movement)
    
    # ball hitting top wall
    if b.ycor() >= 290:
        y_movement = (-1 * y_movement)
        
    # reset the ball if fell over the paddle
    if b.ycor() <= -290:
        b.goto(0,0)
        x_movement = 0.06 * randrange(-5,-1)
        y_movement = 0.06 * randrange(-5,-1)

    target_to_remove = None
    
    if len(array_targets) > 1:
        for t in array_targets:
            deviation = 0
            current_shape = t.shape()
            if current_shape == "big_rectangle":
                deviation = 60
            else:
                deviation = 30
            
            # left of the paddle
            if (b.ycor()-10) <= (t.ycor() + 10) and (b.ycor()-10) >= (t.ycor() -20) and (b.xcor()+10) >= (t.xcor() - deviation) and (t.xcor()-10) < (t.xcor()-deviation):
                x_movement = (-1 * x_movement)
                if t != p:
                    target_to_remove = t
                break
            
            # ball hitting right part of the paddle
            if (b.ycor()-10) <= (t.ycor() + 10) and (b.ycor()-10) >= (t.ycor() -20) and (b.xcor()-10) <= (t.xcor() + deviation) and (t.xcor()+10) > (t.xcor()+deviation):
                x_movement = (-1 * x_movement)
                if t != p:
                    target_to_remove = t
                break
                
            # top of paddle
            if ((b.ycor() -10) <= (t.ycor() + 10) )and ((b.ycor() - 10) >= (t.ycor() - 10)) and ((b.xcor() +10) >= (t.xcor()-deviation)) and ((b.xcor() -10) <= (t.xcor()+deviation)):
                y_movement = (-1 * y_movement)
                if t != p:
                    target_to_remove = t
                break
                
            # bottom of paddle
            if ((b.ycor() +10) >= (t.ycor() - 10) )and ((b.ycor() + 10) <= (t.ycor() + 10)) and ((b.xcor() +10) >= (t.xcor()-deviation)) and ((b.xcor() -10) <= (t.xcor()+deviation)):
                y_movement = (-1 * y_movement)
                if t != p:
                    target_to_remove = t
                break
    else:
        finished = True

    if(target_to_remove != None):
        array_targets.remove(target_to_remove)
        target_to_remove.goto(-1000,0)
        target_to_remove.color("black")
        target_to_remove.clear()
    
    
    if finished==True:
        for i in position_targets():
            array_targets.append(i)
        b.goto(0,0)
        x_movement = 0.06 * randrange(-5,-1)
        y_movement = 0.06 * randrange(-5,-1)


    b.setx(b.xcor()+ x_movement)
    b.sety(b.ycor()+ y_movement)
    
    sc.update()