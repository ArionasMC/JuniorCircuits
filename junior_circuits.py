import pygame
import pygame_gui

from pygame_gui.core import ObjectID
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UIButton
from pygame_gui.elements import UILabel

from core.board import Board
from core.constants import *
from core.component import Component
from components.resistance import Resistance

pygame.init()

pygame.display.set_caption('Junior Circuits')
WIDTH = 800
HEIGHT = 600
window_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(window_size)

background_color = pygame.Color("#FFFBF5")
background = pygame.Surface(window_size)
background.fill(background_color)

board_surface = pygame.Surface((580, 580))
board = Board(12, 12, board_surface, background_color)
board.draw_grid()
print("w,h=",board.gridWidth,board.gridHeight)

board.insert((5,9), SOURCE_ID)
board.update_components()

manager = pygame_gui.UIManager(window_size)
manager.get_theme().load_theme("assets/themes/left_panel_theme.json")

##### GUI Objects #####
left_panel_rect = pygame.Rect(-5, -5, 200, HEIGHT+15)
left_panel = UIPanel(relative_rect=left_panel_rect, manager=manager, object_id="#left_panel")

BUTTON_H = 50
STARTING_Y = 10
TEXT_OFFSET_Y = 20
ELEMENT_OFFSET_Y = 60
r_button_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*1, 150, BUTTON_H)
r_button = UIButton(relative_rect=r_button_rect, manager=manager, text="",
                    object_id=ObjectID(class_id="@left_panel_buttons", object_id="#r_button"),
                    container=left_panel)
r_text_rect = pygame.Rect(20, STARTING_Y, 150, 20)
r_text = UILabel(relative_rect=r_text_rect, manager=manager, container=left_panel, text="Αντίσταση",
                 object_id="#button_texts")

a_button_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*2+ELEMENT_OFFSET_Y*1, 150, BUTTON_H)
a_button = UIButton(relative_rect=a_button_rect, manager=manager, text="",
                    object_id=ObjectID(class_id="@left_panel_buttons", object_id="#a_button"),
                    container=left_panel)
a_text_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*1+ELEMENT_OFFSET_Y*1, 150, 20)
a_text = UILabel(relative_rect=a_text_rect, manager=manager, text="Αμπερόμετρο",
                 object_id="#button_texts")

v_button_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*3+ELEMENT_OFFSET_Y*2, 150, BUTTON_H)
v_button = UIButton(relative_rect=v_button_rect, manager=manager, text="",
                    object_id=ObjectID(class_id="@left_panel_buttons", object_id="#v_button"),
                    container=left_panel)
v_text_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*2+ELEMENT_OFFSET_Y*2, 150, 20)
v_text = UILabel(relative_rect=v_text_rect, manager=manager, text="Βολτόμετρο",
                 object_id="#button_texts")

line_button_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*4+ELEMENT_OFFSET_Y*3, 150, BUTTON_H)
line_button = UIButton(relative_rect=line_button_rect, manager=manager, text="Καλώδιο",
                       object_id=ObjectID(class_id="@left_panel_buttons", object_id="#line_button"),
                       container=left_panel)

led_button_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*5+ELEMENT_OFFSET_Y*4, 150, BUTTON_H)
led_button = UIButton(relative_rect=led_button_rect, manager=manager, text="Λαμπτήρας",
                      object_id=ObjectID(class_id="@left_panel_buttons", object_id="#led_button"),
                      container=left_panel)
led_text_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*4+ELEMENT_OFFSET_Y*4, 150, 20)
led_text = UILabel(relative_rect=led_text_rect, manager=manager, text="Λαμπτήρας", object_id="#button_texts")

switch_button_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*6+ELEMENT_OFFSET_Y*5, 150, BUTTON_H)
switch_button = UIButton(relative_rect=switch_button_rect, manager=manager, text="Διακόπτης",
                      object_id=ObjectID(class_id="@left_panel_buttons", object_id="#switch_button"),
                      container=left_panel)
switch_text_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*5+ELEMENT_OFFSET_Y*5, 150, 20)
switch_text = UILabel(relative_rect=switch_text_rect, manager=manager, text="Διακόπτης", object_id="#button_texts")

delete_button_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*7+ELEMENT_OFFSET_Y*6+20, 150, BUTTON_H*0.6)
delete_button = UIButton(relative_rect=delete_button_rect, manager=manager, text="Διαγραφή",
                         object_id=ObjectID(class_id="@left_panel_buttons", object_id="#delete_button"), container=left_panel)

delete_all_button_rect = pygame.Rect(20, STARTING_Y+TEXT_OFFSET_Y*8+ELEMENT_OFFSET_Y*7-30, 150, BUTTON_H*0.6)
delete_all_button = UIButton(relative_rect=delete_all_button_rect, manager=manager, text="Διαγραφή Όλων",
                             object_id=ObjectID(class_id="@left_panel_buttons", object_id="#delete_all_button"),
                             container=left_panel)

clock = pygame.time.Clock()
debug_mode = False
running = True

show_available = False
current_id = EMPTY_ID
first_point = (0,0)
second_time = False
deletion_time = False

test_surface = pygame.Surface((100,100))
test_rect = pygame.Rect(0,0,100,100)
pygame.draw.rect(surface=test_surface, color=pygame.Color(0,0,0,255), rect=test_rect)

mouse_rect = pygame.Rect(0,0,49,49)
mouse_component = 0
rotated_component = False

def toggle_available_points():
    global show_available
    global current_id
    show_available = ~show_available
    board.erase_and_clear_points()
    if show_available:
        board.update_available_points(current_id)

def toggle_second_wire_points():
    global show_available
    global first_point
    global second_time
    show_available = ~show_available
    second_time = ~second_time
    board.erase_and_clear_points()
    if show_available:
        board.update_points_for_second_wire(first_point)

def toggle_deletion_points():
    global show_available
    global deletion_time
    show_available = ~show_available
    deletion_time = ~deletion_time
    board.erase_and_clear_points()
    if deletion_time:
        board.update_points_for_deletion()

# Only horizontal and vertical lines are allowed (for simplicity)
def place_wires(first_point, second_point):
    (x1, y1) = first_point
    (x2, y2) = second_point
    if y1 == y2: # horizontal line
        x_min = min(x1, x2)
        x_max = max(x1, x2)
        while x_min <= x_max:
            if board.is_empty_at(x_min, y1):
                board.insert((x_min, y1), LINE_ID)
            x_min += 1
    else: # vertical line
        y_min = min(y1, y2)
        y_max = max(y1, y2)
        while y_min <= y_max:
            if board.is_empty_at(x1, y_min):
                board.insert((x1, y_min), LINE_ID)
            y_min +=1
    board.update_components()

while running:
    time_delta = clock.tick(60)/1000.0

    mouse_rect.x = pygame.mouse.get_pos()[0] - mouse_rect.w/2
    mouse_rect.y = pygame.mouse.get_pos()[1] - mouse_rect.h/2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                debug_mode = ~debug_mode
                manager.set_visual_debug_mode(debug_mode)
            if event.key == pygame.K_r:
                toggle_available_points()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if show_available:
                toggle_available_points()
            if deletion_time:
                deletion_time = False
            if second_time:
                second_time = False
            if event.ui_element == r_button:
                current_id = RESISTANCE_ID
                mouse_component = Resistance(mouse_rect.x, mouse_rect.y, 0)
                if not(show_available):
                    toggle_available_points()
            if event.ui_element == a_button:
                current_id = AMPEROMETER_ID
                mouse_component = Component("assets/sprites/amperometer.png", mouse_rect.x, mouse_rect.y, True)
                if not(show_available):
                    toggle_available_points()
            if event.ui_element == v_button:
                current_id = VOLTOMETER_ID
                mouse_component = Component("assets/sprites/voltometer.png", mouse_rect.x, mouse_rect.y, True)
                if not(show_available):
                    toggle_available_points()
            if event.ui_element == line_button:
                current_id = LINE_ID
                mouse_component = Component("assets/sprites/line.png", mouse_rect.x, mouse_rect.y, True)
                if not(show_available):
                    toggle_available_points()
            if event.ui_element == delete_button:
                current_id = EMPTY_ID
                mouse_component = 0
                if not(deletion_time):
                    toggle_deletion_points()
            if event.ui_element == delete_all_button:
                current_id = EMPTY_ID
                mouse_component = 0
                board.clear_board()
                board.update_components()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_available:
                if event.button == LEFT_CLICK:
                    mx, my = pygame.mouse.get_pos()
                    print(mx, my)
                    for point in board.points:
                        if point.clicked_me(mx, my):
                            if(deletion_time):
                                toggle_deletion_points()
                                board.insert((point.i, point.j), 0)
                                board.update_components()
                                current_id = EMPTY_ID
                                mouse_component = 0
                            else:
                                if current_id == LINE_ID:
                                    if second_time:
                                        second_point = (point.i, point.j)
                                        place_wires(first_point, second_point)
                                        toggle_second_wire_points()
                                    else:
                                        first_point = (point.i, point.j)
                                        toggle_available_points() # remove points
                                        toggle_second_wire_points() # show wire points
                                    mouse_component = 0
                                else:
                                    print('i,j=',point.i,point.j) 
                                    toggle_available_points()
                                    board.insert((point.i, point.j), current_id, rotated_component)
                                    board.update_components()
                                    current_id = EMPTY_ID
                                    mouse_component = 0
                                    rotated_component = False
                elif event.button == RIGHT_CLICK:
                    #print('right click')
                    if (mouse_component != 0) and (get_id_from_component(mouse_component) in ORIENTED_COMPONENT_IDS):
                        # Rotate component on mouse
                        print('rotating')
                        rotated_component = ~rotated_component
                        mouse_component.surface = pygame.transform.rotate(mouse_component.surface, VERTICAL_ROTATION)

        manager.process_events(event)

    manager.update(time_delta)

    screen.blit(background, (0, 0))    
    screen.blit(board.surface, (210, 10))

    for (com, cell) in board.components:
        screen.blit(com.surface, (210+com.posX, 10+com.posY))

    for wire in board.wires:
        screen.blit(wire.surface, (210+wire.surface_x, 10+wire.surface_y))

    if show_available:
        for point in board.points:
            posX = (point.i+0.5)*board.gridWidth-point.rect.w/2+210
            posY = (point.j+0.5)*board.gridHeight-point.rect.h/2+10
            screen.blit(point.surface, (posX, posY))
            point.rect = pygame.Rect(posX, posY, POINT_SIZE, POINT_SIZE)

    if mouse_component != 0:
        if current_id == LINE_ID:
            mouse_rect.y += mouse_rect.h/2
        screen.blit(mouse_component.surface, (mouse_rect.x, mouse_rect.y))
    #pygame.draw.rect(surface=screen, color=pygame.Color(0,0,0), rect=mouse_rect)

    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()