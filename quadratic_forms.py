import numpy as np
import pygame as pg

WIDTH, HEIGHT = 1200, 800
EDGE_LENGTH = 200
EDGE_LENGTH_SCALE = 0.8
FONT_SIZE = 14
ANGLE = np.pi / 6
DEPTH = 5

start_point = np.array([WIDTH // 2, HEIGHT // 2])
e1 = np.array([int(i) for i in input("insert vector e1\n").split()])
e2 = np.array([int(i) for i in input("insert vector e2\n").split()])
A, B, C = [int(i) for i in input("insert coeffs A, B, C: Ax^2 + Bxy + Cy^2\n").split()]
f_e1 = A*e1[0]**2 + B*e1[0]*e1[1] + C*e1[1]**2
f_e2 = A*e2[0]**2 + B*e2[0]*e2[1] + C*e2[1]**2
f_e1_plus_e2 = A*(e1[0] + e2[0])**2 + B*(e1[0] + e2[0])*(e1[1] + e2[1]) + C*(e1[1] + e2[1])**2

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Fractal Tree")
font = pg.font.SysFont(None, FONT_SIZE)
clock = pg.time.Clock()
COLOR_LINE, COLOR_TEXT = pg.Color(100, 0, 0), pg.Color("black")

def rotate_vector(vector, angle):
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    return np.dot(rotation_matrix, vector)


def get_perpendicular(vector):
    return np.array([-vector[1], vector[0]])


def draw_text(screen, text, position, direction):
    perp_vector = get_perpendicular(direction)
    perp_vector = perp_vector / np.linalg.norm(perp_vector) * 20  # Нормализуем и масштабируем
    text_position = position + perp_vector
    text_surface = font.render(text, True, COLOR_TEXT)
    screen.blit(text_surface, text_position)


def get_up(e_up, e_down, e_c, f_e_up, f_e_down, f_e_c):
    new_up = e_up
    new_down = e_c
    new_c = e_up + e_c
    a, b, d = f_e_up, f_e_c, f_e_down
    c = 2 * (a + b) - d
    new_f_up, new_f_down, new_f_c = a, b, c
    return new_up, new_down, new_c, new_f_up, new_f_down, new_f_c


def get_down(e_up, e_down, e_c, f_e_up, f_e_down, f_e_c):
    new_up = e_c
    new_down = e_down
    new_c = e_down + e_c
    a, b, d = f_e_c, f_e_down, f_e_up
    c = 2 * (a + b) - d
    new_f_up, new_f_down, new_f_c = a, b, c
    return new_up, new_down, new_c, new_f_up, new_f_down, new_f_c


def draw_symmetric_fractal_tree_with_text(e_up, e_down, e_c, f_e_up, f_e_down, f_e_c, part, start, direction, depth,
                                          length=EDGE_LENGTH, angle=ANGLE):
    if depth == 0:
        return

    end_point = start + direction * length
    pg.draw.aaline(screen, COLOR_LINE, start, end_point)

    mid_point = (start + end_point) / 2
    text_surface = font.render(f"{f_e_c - (f_e_up + f_e_down)}", True, COLOR_TEXT)
    screen.blit(text_surface, mid_point)
    if part == 0:
        draw_text(screen, f"Q({e_up[0]}, {e_up[1]}) = {f_e_up}", mid_point, -direction)
        draw_text(screen, f"Q({e_down[0]}, {e_down[1]}) = {f_e_down}", mid_point, direction)
    else:
        draw_text(screen, f"Q({e_up[0]}, {e_up[1]}) = {f_e_up}", mid_point, direction)
        draw_text(screen, f"Q({e_down[0]}, {e_down[1]}) = {f_e_down}", mid_point, -direction)

    new_direction = rotate_vector(direction, angle)
    if part == 1:
        new_up, new_down, new_c, new_f_up, new_f_down, new_f_c = get_up(e_up, e_down, e_c, f_e_up, f_e_down, f_e_c)
    else:
        new_up, new_down, new_c, new_f_up, new_f_down, new_f_c = get_down(e_up, e_down, e_c, f_e_up, f_e_down, f_e_c)

    draw_symmetric_fractal_tree_with_text(new_up, new_down, new_c, new_f_up, new_f_down, new_f_c, part, end_point,
                                          new_direction, depth - 1, length * EDGE_LENGTH_SCALE, angle)

    new_direction = rotate_vector(direction, -angle)
    if part == 1:
        new_up, new_down, new_c, new_f_up, new_f_down, new_f_c = get_down(e_up, e_down, e_c, f_e_up, f_e_down, f_e_c)
    else:
        new_up, new_down, new_c, new_f_up, new_f_down, new_f_c = get_up(e_up, e_down, e_c, f_e_up, f_e_down, f_e_c)

    draw_symmetric_fractal_tree_with_text(new_up, new_down, new_c, new_f_up, new_f_down, new_f_c, part, end_point,
                                          new_direction, depth - 1, length * EDGE_LENGTH_SCALE, angle)

def Draw(start):
    e1_plus_e2 = e1 + e2
    _e2 = -e2
    f__e2 = f_e2
    e1_minus_e2 = e1 - e2
    f_e1_minus_e2 = 2 * (f_e1 + f_e2) - f_e1_plus_e2
    length = EDGE_LENGTH
    angle = ANGLE
    initial_direction_right = np.array([1, 0])
    initial_direction_left = np.array([-1, 0])

    left_start, right_start = start - initial_direction_right * length / 2, start + initial_direction_right * length / 2
    pg.draw.aaline(screen, COLOR_LINE, left_start, right_start)

    draw_text(screen, f"Q({e1[0]}, {e1[1]}) = {f_e1}", start, -initial_direction_right)
    draw_text(screen, f"Q({e2[0]}, {e2[1]}) = {f_e2}", start, initial_direction_right)

    # right direction: up = e1, down = e2, c = e1_plus_e2

    new_direction = rotate_vector(initial_direction_right, angle)
    new_up, new_down, new_c, new_f_up, new_f_down, new_f_c = get_down(e1, e2, e1_plus_e2, f_e1, f_e2, f_e1_plus_e2)
    draw_symmetric_fractal_tree_with_text(new_up, new_down, new_c, new_f_up, new_f_down, new_f_c, 0, right_start,
                                          new_direction, DEPTH - 1, length * EDGE_LENGTH_SCALE, angle)
    new_direction = rotate_vector(initial_direction_right, -angle)
    new_up, new_down, new_c, new_f_up, new_f_down, new_f_c = get_up(e1, e2, e1_plus_e2, f_e1, f_e2, f_e1_plus_e2)
    draw_symmetric_fractal_tree_with_text(new_up, new_down, new_c, new_f_up, new_f_down, new_f_c, 0, right_start,
                                          new_direction, DEPTH - 1, length * EDGE_LENGTH_SCALE, angle)

    # left direction: up = e1, down = _e2, c = e1_minus_e2

    new_direction = rotate_vector(initial_direction_left, angle)
    new_up, new_down, new_c, new_f_up, new_f_down, new_f_c = get_up(e1, _e2, e1_minus_e2, f_e1, f__e2, f_e1_minus_e2)
    draw_symmetric_fractal_tree_with_text(new_up, new_down, new_c, new_f_up, new_f_down, new_f_c, 1, left_start,
                                          new_direction, DEPTH - 1, length * EDGE_LENGTH_SCALE, angle)

    new_direction = rotate_vector(initial_direction_left, -angle)
    new_up, new_down, new_c, new_f_up, new_f_down, new_f_c = get_down(e1, _e2, e1_minus_e2, f_e1, f__e2, f_e1_minus_e2)
    draw_symmetric_fractal_tree_with_text(new_up, new_down, new_c, new_f_up, new_f_down, new_f_c, 1, left_start,
                                          new_direction, DEPTH - 1, length * EDGE_LENGTH_SCALE, angle)


running = True
screen.fill((255, 255, 255))
Draw(start_point)
pg.display.flip()
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    clock.tick(30)

pg.quit()
