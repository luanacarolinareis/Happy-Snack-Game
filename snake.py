import time
import random
import functools
import turtle

MAX_X = 600
MAX_Y = 800
DEFAULT_SIZE = 20
SNAKE_SHAPE = 'square'
HIGH_SCORES_FILE_PATH = 'high_scores.txt'
# Controla a velocidade da cobra. Quanto menor o valor, mais rápido é o movimento da cobra.
speed = 0.25
turtle.title("Happy Snack Game")
foods = ['banana.gif', 'bread.gif', 'candy.gif', 'chocolate.gif', 'cookie.gif',
         'donut.gif', 'doritos.gif', 'egg.gif', 'pizza.gif', 'popcorn.gif']


def load_high_score(state):
    # se já existir um high score devem guardar o valor em state['high_score']
    if state['high_score'] < state['score']:
        state['high_score'] = state['score']
    return state['high_score']


def write_high_score_to_file(state):
    # devem escrever o valor que está em state['high_score'] no ficheiro de high scores
    f = open(HIGH_SCORES_FILE_PATH, 'w')
    f.seek(0)
    f.truncate()
    f.write(str(load_high_score(state)))
    f.close()


def create_score_board(state):
    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.shape("square")
    score_board.color('white')
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0, MAX_Y / 2.3)
    state['score_board'] = score_board
    load_high_score(state)
    update_score_board(state)


def update_score_board(state):
    file = open(HIGH_SCORES_FILE_PATH, "r")
    state['score_board'].clear()
    state['score_board'].write("Score: {} High Score: {}".format(state['score'], file.readline()), align="center",
                               font=("Helvetica", 24, "normal"))
    file.close()


def go_up(state):
    if state['snake']['current_direction'] != 'down':
        state['snake']['current_direction'] = 'up'


def go_down(state):
    if state['snake']['current_direction'] != 'up':
        state['snake']['current_direction'] = 'down'


def go_left(state):
    if state['snake']['current_direction'] != 'right':
        state['snake']['current_direction'] = 'left'


def go_right(state):
    if state['snake']['current_direction'] != 'left':
        state['snake']['current_direction'] = 'right'


def init_state():
    segments = []  # Lista que vai armazenar os segmentos do corpo
    file = open(HIGH_SCORES_FILE_PATH, "r")

    state = {'score_board': None, 'new_high_score': False, 'high_score': int(file.readline()), 'score': 0, 'food': None, 'window': None,
             'body': segments, 'level': turtle.Turtle()}
    file.close()
    # Informação necessária para a criação do score board
    # Para gerar a comida deverá criar uma nova tartaruga e colocar a mesma numa posição aleatória do campo
    snake = {
        'head': None,  # Variável que corresponde à cabeça da cobra
        'current_direction': None  # Indicação da direção atual do movimento da cobra
    }
    state['snake'] = snake
    return state


def setup(state):
    window = turtle.Screen()
    window.setup(width=MAX_X, height=MAX_Y, starty=0)
    window.bgcolor(27 / 255, 94 / 255, 32 / 255)
    window.bgpic('snake_600_800.png')
    window.addshape('block_body.gif')
    window.addshape('level.gif')
    for i in foods:
        window.addshape(i)
    window.listen()
    keyboard = ['w', 'a', 's', 'd', 'W', 'A', 'S', 'D', 'Up', 'Left', 'Down', 'Right']
    for i in range(0, len(keyboard), 4):
        window.onkey(functools.partial(go_up, state), keyboard[i])
        window.onkey(functools.partial(go_left, state), keyboard[i + 1])
        window.onkey(functools.partial(go_down, state), keyboard[i + 2])
        window.onkey(functools.partial(go_right, state), keyboard[i + 3])
    window.tracer(0)
    state['window'] = window

    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Turtle()
    snake['head'].shape(SNAKE_SHAPE)
    snake['head'].pu()
    snake['head'].color('green')

    create_score_board(state)
    create_food(state)


def move(state):
    """
    Função responsável pelo movimento da cobra no ambiente.
    """
    snake = state['snake']
    if state['snake']['current_direction'] == 'up':
        snake['head'].setheading(90)
        snake['head'].fd(20)
    if state['snake']['current_direction'] == 'left':
        snake['head'].setheading(180)
        snake['head'].fd(20)
    if state['snake']['current_direction'] == 'right':
        snake['head'].setheading(0)
        snake['head'].fd(20)
    if state['snake']['current_direction'] == 'down':
        snake['head'].setheading(-90)
        snake['head'].fd(20)


def create_food(state):
    """
    Função responsável pela criação da comida. Note que elas deverão ser colocadas em posições aleatórias,
    mas dentro dos limites do ambiente.
    """
    # a informação sobre a comida deve ser guardada em state['food']

    x = random.randint(-13, 13) * 20
    y = random.randint(-18, 17) * 20

    state['food'] = turtle.Turtle()
    state['food'].shape(random.choice(foods))
    state['food'].pu()
    state['food'].goto(x, y)
    state['food'].color('red')

    check_food_body_collisions(state)
    return state['food']


def check_if_food_to_eat(state):
    """
    Função responsável por verificar se a cobra tem uma peça de comida para comer. Deverá considerar que se a comida
    estiver a uma distância inferior a 15 píxeis a cobra pode comer a peça de comida.
    """
    global speed
    food = state['food']
    snake = state['snake']
    segments = state['body']
    if snake['head'].distance(food) < 15:
        food.hideturtle()  # Esconde a comida "apanhada"
        create_food(state)  # Gera uma nova comida

        # Adição de um novo segmento corporal à lista "segments"
        body_segment = turtle.Turtle()
        body_segment.shape('block_body.gif')
        body_segment.pu()
        body_segment.color('black')
        segments.append(body_segment)

        state['score'] += 10
        if state['score'] % 200 == 0 and 0 < state['score'] <= 1000:
            if speed > 0.05:
                speed -= 0.04
        write_high_score_to_file(state)
    # para ler ou escrever os valores de high score, score e new high score, devem usar os respetivos campos do
    # state: state['high_score'], state['score'] e state['new_high_score']


def boundaries_collision(state):
    """
    Função responsável por verificar se a cobra colidiu com os limites do ambiente. Sempre que isto acontecer a
    função deverá returnar o valor booleano True, caso contrário retorna False.
    """
    global speed
    snake = state['snake']
    food = state['food']
    segments = state['body']

    # Se a cabeça da cobra ultrapassou os limites do ambiente...
    if snake['head'].xcor() > 280 or snake['head'].xcor() < -280 or snake['head'].ycor() > 380 or snake['head'].ycor() < -380:
        snake['head'].ht()
        food.hideturtle()
        for i in segments:
            i.hideturtle()
        state['level'].ht()
        speed = 0.25
        return True
    return False


def check_collisions(state):
    """
    Função responsável por avaliar se há colisões. Atualmente apenas chama a função que verifica se há colisões com
    os limites do ambiente. No entanto, deverá escrever o código para verificar quando é que a tartaruga choca com uma
    parede ou com o seu corpo.
    """
    global speed
    snake = state['snake']
    food = state['food']
    segments = state['body']

    for i in segments:
        if i.distance(snake['head']) < 15:
            snake['head'].ht()
            food.hideturtle()
            for j in segments:
                j.hideturtle()
            state['level'].ht()
            speed = 0.25
            return True
    return boundaries_collision(state)


# Função que verifica se a comida foi gerada dentro de alguma das partes do corpo
def check_food_body_collisions(state):
    food = state['food']
    segments = state['body']
    for i in segments:
        if i.distance(food) < 15:  # Em caso disso ocorrer, cria uma comida nova (noutro local)
            food.hideturtle()
            create_food(state)
    if food.distance(state['level']) < 25:  # EXTRA (colisões com o ícone de level up)
        food.hideturtle()
        create_food(state)

# Aumenta a velocidade do jogo consoante a pontuação (existem 5 níveis possíveis)
def level_up(state):
    state['level'].pu()
    state['level'].setposition(-150, -200)
    state['level'].shape('level.gif')
    state['level'].ht()

    if state['score'] % 200 == 0 and 0 < state['score'] <= 1000:
        state['level'].st()
    else:
        state['level'].ht()


def main():
    while True:
        state = init_state()
        setup(state)
        snake = state['snake']
        segments = state['body']

        while not check_collisions(state):
            state['window'].update()
            check_if_food_to_eat(state)
            update_score_board(state)
            level_up(state)
            for i in range(len(segments) - 1, -1, -1):  # Percorre todos os segmentos do corpo, do mais recente para o mais antigo
                # O primeiro segmento adicionado vai receber as coordenadas da cabeça
                if i == 0:
                    x = snake['head'].xcor()
                    y = snake['head'].ycor()
                # Cada um dos segmentos seguintes vai receber as coordenadas do segmento anterior
                else:
                    x = segments[i - 1].xcor()
                    y = segments[i - 1].ycor()
                segments[i].goto(x, y)
            move(state)
            time.sleep(speed)
        print("YOU LOSE!")
        state['score_board'].clear()


main()

# Nome: Luana Carolina Cunha Reis
# Nº de estudante: 2022220606

# Nome: Diogo Ramos Barbosa
# Nº de estudante: 2021234034

'''

Referências:
Fundo do jogo: https://wallpapercave.com/cartoon-snake-wallpapers
Corpo da snake: https://github.com/codebasics/python_projects/blob/main/1_snake_game/resources/block.jpg
Templates das comidas: https://www.canva.com/

'''
