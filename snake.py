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
SPEED = 0.5


def load_high_score(state):
    # se já existir um high score devem guardar o valor em state['high_score']
    pass

def write_high_score_to_file(state):
    # devem escrever o valor que está em state['high_score'] no ficheiro de high scores
    pass

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
    state['score_board'].clear()
    state['score_board'].write("Score: {} High Score: {}".format(state['score'], state['high_score']), align="center", font=("Helvetica", 24, "normal"))

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
    state = {'score_board': None, 'new_high_score': False, 'high_score': 0, 'score': 0, 'food': None, 'window': None}
    # Informação necessária para a criação do score board
    # Para gerar a comida deverá criar uma nova tartaruga e colocar a mesma numa posição aleatória do campo
    snake = {
        'head': None,                  # Variável que corresponde à cabeça da cobra
        'current_direction': None   # Indicação da direção atual do movimento da cobra
    }
    state['snake'] = snake
    return state

def setup(state):
    window = turtle.Screen()
    window.setup(width=MAX_X, height=MAX_Y)
    window.listen()
    window.onkey(functools.partial(go_up, state), 'w')
    window.onkey(functools.partial(go_down, state), 's')
    window.onkey(functools.partial(go_left, state), 'a')
    window.onkey(functools.partial(go_right, state), 'd')
    window.tracer(0)
    state['window'] = window
    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Turtle()
    snake['head'].shape(SNAKE_SHAPE)
    snake['head'].showturtle()
    snake['head'].pu()
    snake['head'].color('green')

    # ADICIONADO
    snake['body'] = turtle.Turtle()
    snake['body'].shape(SNAKE_SHAPE)
    snake['body'].showturtle()
    snake['body'].pu()
    snake['body'].goto(-20, 0)
    snake['body'].color('black')
    # ADICIONADO

    create_score_board(state)
    create_food(state)

def move(state):
    """
    Função responsável pelo movimento da cobra no ambiente.
    """
    snake = state['snake']

    # ADICIONADO
    print(snake['head'].xcor())
    print(snake['body'].xcor())

    snake['head'].fd(20)
    snake['body'].fd(20)
    # ADICIONADO


def create_food(state):
    """
    Função responsável pela criação da comida. Note que elas deverão ser colocadas em posições aleatórias,
    mas dentro dos limites do ambiente.
    """
    # a informação sobre a comida deve ser guardada em state['food']

def check_if_food_to_eat(state):
    """
    Função responsável por verificar se a cobra tem uma peça de comida para comer. Deverá considerar que se a comida
    estiver a uma distância inferior a 15 píxeis a cobra pode comer a peça de comida.
    """
    food = state['food']
    # para ler ou escrever os valores de high score, score e new high score, devem usar os respetivos campos do
    # state: state['high_score'], state['score'] e state['new_high_score']

def boundaries_collision(state):
    """
    Função responsável por verificar se a cobra colidiu com os limites do ambiente. Sempre que isto acontecer a
    função deverá returnar o valor booleano True, caso contrário retorna False.
    """
    return False

def check_collisions(state):
    """
    Função responsável por avaliar se há colisões. Atualmente apenas chama a função que verifica se há colisões com
    os limites do ambiente. No entanto, deverá escrever o código para verificar quando é que a tartaruga choca com uma
    parede ou com o seu corpo.
    """
    snake = state['snake']
    return boundaries_collision(state)

def main():
    state = init_state()
    setup(state)
    while not check_collisions(state):
        state['window'].update()
        check_if_food_to_eat(state)
        move(state)
        time.sleep(SPEED) 
    print("YOU LOSE!")
    if state['new_high_score']:
        write_high_score_to_file(state)


main()
