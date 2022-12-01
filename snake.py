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
SPEED = 0.1


def load_high_score(state):
    # se já existir um high score devem guardar o valor em state['high_score']
    if state['high_score'] < state['score']:
        state['high_score'] = state['score']
    return state['high_score']

def write_high_score_to_file(state):
    # devem escrever o valor que está em state['high_score'] no ficheiro de high scores
    with open('file_score.txt', 'w') as f:
        f.seek(0)
        f.truncate()
        f.write(str(load_high_score(state)))
    f.close()


def create_score_board(state):
    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.shape("square")
    score_board.color("black")
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0, MAX_Y / 2.2)
    state['score_board'] = score_board
    load_high_score(state)
    update_score_board(state)


def update_score_board(state):
    file = open("file_score.txt", "r")
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
    file = open("file_score.txt", "r")

    state = {'score_board': None, 'new_high_score': False, 'high_score': int(file.readline()), 'score': 0, 'food': None, 'window': None,
             'body': segments}
    # Informação necessária para a criação do score board
    # Para gerar a comida deverá criar uma nova tartaruga e colocar a mesma numa posição aleatória do campo
    snake = {
        'head': None,  # Variável que corresponde à cabeça da cobra
        'current_direction': None  # Indicação da direção atual do movimento da cobra
    }
    state['snake'] = snake
    file.close()
    return state


def setup(state):
    window = turtle.Screen()
    window.setup(width=MAX_X, height=MAX_Y)
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
    segments = state['body']
    # a informação sobre a comida deve ser guardada em state['food']

    x = random.randint(-12, 12) * 20
    y = random.randint(-17, 17) * 20

    state['food'] = turtle.Turtle()
    state['food'].shape('circle')
    state['food'].pu()
    state['food'].goto(x, y)
    state['food'].color('red')
    return state['food']


def check_if_food_to_eat(state):
    """
    Função responsável por verificar se a cobra tem uma peça de comida para comer. Deverá considerar que se a comida
    estiver a uma distância inferior a 15 píxeis a cobra pode comer a peça de comida.
    """
    food = state['food']
    snake = state['snake']
    segments = state['body']

    if snake['head'].distance(food) < 15:
        food.hideturtle()  # Esconde a comida "apanhada"
        create_food(state)  # Gera uma nova comida

        # Adição de um novo segmento corporal à lista "segments"
        body_segment = turtle.Turtle()
        body_segment.shape(SNAKE_SHAPE)
        body_segment.pu()
        body_segment.color('black')
        segments.append(body_segment)

        state['score'] += 10
        write_high_score_to_file(state)

    # para ler ou escrever os valores de high score, score e new high score, devem usar os respetivos campos do
    # state: state['high_score'], state['score'] e state['new_high_score']


def boundaries_collision(state):
    """
    Função responsável por verificar se a cobra colidiu com os limites do ambiente. Sempre que isto acontecer a
    função deverá returnar o valor booleano True, caso contrário retorna False.
    """
    snake = state['snake']
    food = state['food']
    segments = state['body']

    # Se a cabeça da cobra ultrapassou os limites do ambiente...
    if snake['head'].xcor() > 300 or snake['head'].xcor() < -300 or snake['head'].ycor() > 400 or snake['head'].ycor() < -400:
        snake['head'].ht()
        food.hideturtle()
        for i in segments:
            i.hideturtle()
        return True
    return False


def check_collisions(state):
    """
    Função responsável por avaliar se há colisões. Atualmente apenas chama a função que verifica se há colisões com
    os limites do ambiente. No entanto, deverá escrever o código para verificar quando é que a tartaruga choca com uma
    parede ou com o seu corpo.
    """
    snake = state['snake']
    food = state['food']
    segments = state['body']

    for i in segments:
        if i.distance(snake['head']) < 15:
            snake['head'].ht()
            food.hideturtle()
            for j in segments:
                j.hideturtle()
            return True
    return boundaries_collision(state)


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
            time.sleep(SPEED)
        print("YOU LOSE!")
        state['score_board'].clear()

        if state['new_high_score']:
            write_high_score_to_file(state)


main()

# Nome: Luana Carolina Cunha Reis
# Nº de estudante: 2022220606

# Nome: Diogo Ramos Barbosa
# Nº de estudante: 2021234034
