import math
from scipy import constants

ball_mass = 0  # kg
ball_start_velocity = 0  # m/s
box_mass = 0  # kg
box_stop_x = 0
ANGLE = 45  # degrees
FRICTION_COEFFICIENT = 0.58  # concrete
GRAVITY_STRENGTH = 9.8
height = 250

BALL_MAX_MASS = 220
BALL_MAX_VELOCITY = constants.speed_of_light


def emulate(m1: float, m2: float, v: float):
    if input_is_valid(m1, m2, v):
        global ball_mass
        ball_mass = m1
        global box_mass
        box_mass = m2
        global ball_start_velocity
        ball_start_velocity = v
        print("Высота по умолчанию {} метров".format(height))
        print("Пройденное растояние: {} метров".format(round(calculateDistance(), 2)))
        return True
    else:
        print("Введено некорректное значение")
        return False


def set_values(m1: float, m2: float, v: float, h: int):
    if input_is_valid(m1, m2, v):
        global ball_mass
        ball_mass = m1
        global box_mass
        box_mass = m2
        global ball_start_velocity
        ball_start_velocity = v
        global height
        height = h


def calculateDistance():
    box_velocity = (ball_mass * get_final_ball_velocity() * math.sin(math.radians(ANGLE))) / (ball_mass + box_mass)
    print("Ящик развил скорость: {} м/c".format(round(box_velocity), 2))
    friction = 2 * FRICTION_COEFFICIENT * GRAVITY_STRENGTH
    distance = math.pow(box_velocity, 2) / friction
    return distance


def input_is_valid(m1, m2, v):
    if BALL_MAX_MASS < m1 or m1 <= 0:
        print(" [!]Ошибка: \n [!]Масса ядра должна быть положительной и не превышать {} кг".format(BALL_MAX_MASS))
        return False
    if m2 <= 0:
        print(" [!]Ошибка: \n [!]Масса ящика должна быть положительной")
        return False
    if BALL_MAX_VELOCITY < v or v <= 0:
        print(" [!]Ошибка: \n [!]Скорость должна быть положительной и не превышать {} м/с".format(BALL_MAX_VELOCITY))
        return False
    return True


def get_ball_position(time):
    hor_velocity = ball_start_velocity * math.sin(math.radians(ANGLE))
    vert_velocity = ball_start_velocity * math.cos(math.radians(ANGLE))

    gravity_acceleration = (GRAVITY_STRENGTH * math.pow(time, 2)) / 2

    x = (ball_start_velocity + hor_velocity) * time
    y = height - vert_velocity * time - gravity_acceleration
    return [x, y]


def get_ball_velocity(time):
    gravity_deflection = 2 * ball_start_velocity * GRAVITY_STRENGTH * time * math.cos(math.radians(ANGLE))
    gravity_affection = GRAVITY_STRENGTH * GRAVITY_STRENGTH * time * time
    vt = ball_start_velocity - gravity_deflection + gravity_affection
    return vt


def get_box_x0():
    hor_velocity = ball_start_velocity * math.sin(math.radians(ANGLE))
    vert_velocity = ball_start_velocity * math.cos(math.radians(ANGLE))
    gravity_affection = math.sqrt((2 * (height - vert_velocity)) / GRAVITY_STRENGTH)
    x0 = hor_velocity * gravity_affection
    return x0


def get_final_ball_velocity():
    hor_velocity = ball_start_velocity * math.sin(math.radians(ANGLE))
    vert_velocity = ball_start_velocity * math.cos(math.radians(ANGLE))
    lower_sqrt = math.sqrt(2 * GRAVITY_STRENGTH * (height - vert_velocity))
    v_final = math.sqrt(math.pow(hor_velocity, 2) + math.pow((-vert_velocity - lower_sqrt), 2))
    return v_final
    

def get_box_start_velocity():
    dividend = ball_mass * get_final_ball_velocity() * math.sin(math.radians(ANGLE))
    divider = ball_mass + box_mass
    start_velocity = dividend / divider
    return start_velocity


def get_box_current_velocity(time):
    vt = get_box_start_velocity() - GRAVITY_STRENGTH * FRICTION_COEFFICIENT * time
    if vt < 0:
        vt = 0
    return vt


def get_box_pos(time):
    global box_stop_x
    x0 = get_box_x0()
    fr_grav_deflection = (GRAVITY_STRENGTH * FRICTION_COEFFICIENT * math.pow(time, 2)) / 2
    if get_box_current_velocity(time) > 0:
        xt = x0 + get_box_start_velocity() * time - fr_grav_deflection
        box_stop_x = xt
    return box_stop_x
