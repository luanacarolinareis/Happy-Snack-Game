import turtle as t
snake = t.Turtle()
snake.shape('square')
snake.color('green')
snake.pu()

food = t.Turtle()
snake.shape('circle')
food.color('red')
food.pu()
food.goto(10, 10)

print(snake.distance(food))
print(food.distance(snake))
if snake.distance(food) < 15:
    print('Happy snack:  ')
    food.goto(-50, -50)
else:
    print('Sad snack:(')
t.exitonclick()
