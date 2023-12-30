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

r_button_rect = pygame.Rect(20, 50, 150, 60)
r_button = UIButton(relative_rect=r_button_rect, manager=manager, text="",
                    object_id=ObjectID(class_id="@left_panel_buttons", object_id="#r_button"),
                    container=left_panel)
r_text_rect = pygame.Rect(20, 30, 150, 20)
r_text = UILabel(relative_rect=r_text_rect, manager=manager, container=left_panel, text="Αντίσταση",
                 object_id="#button_texts")

a_button_rect = pygame.Rect(20, 160, 150, 60)
a_button = UIButton(relative_rect=a_button_rect, manager=manager, text="",
                    object_id=ObjectID(class_id="@left_panel_buttons", object_id="#a_button"),
                    container=left_panel)
a_text_tect = pygame.Rect(20, 140, 150, 20)
a_text = UILabel(relative_rect=a_text_tect, manager=manager, text="Αμπερόμετρο",
                 object_id="#button_texts")

v_button_rect = pygame.Rect(20, 270, 150, 60)
v_button = UIButton(relative_rect=v_button_rect, manager=manager, text="",
                    object_id=ObjectID(class_id="@left_panel_buttons", object_id="#v_button"),
                    container=left_panel)
v_text_tect = pygame.Rect(20, 250, 150, 20)
v_text = UILabel(relative_rect=v_text_tect, manager=manager, text="Βολτόμετρο",
                 object_id="#button_texts")

clock = pygame.time.Clock()
debug_mode = False
running = True

show_available = False
current_id = EMPTY_ID

test_surface = pygame.Surface((100,100))
test_rect = pygame.Rect(0,0,100,100)
pygame.draw.rect(surface=test_surface, color=pygame.Color(0,0,0,255), rect=test_rect)

mouse_rect = pygame.Rect(0,0,49,49)
mouse_component = 0

def toggle_available_points():
    global show_available
    show_available = ~show_available
    board.erase_and_clear_points()
    if show_available:
        board.update_available_points()

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
            if event.ui_element == r_button:
                current_id = RESISTANCE_ID
                mouse_component = Resistance(mouse_rect.x, mouse_rect.y, 0)
                if not(show_available):
                    toggle_available_points()
            if event.ui_element == a_button:
                current_id = AMPEROMETER_ID
                mouse_component = Component("assets/sprites/amperometer.png", mouse_rect.x, mouse_rect.y)
                if not(show_available):
                    toggle_available_points()
            if event.ui_element == v_button:
                current_id = VOLTOMETER_ID
                mouse_component = Component("assets/sprites/voltometer.png", mouse_rect.x, mouse_rect.y)
                if not(show_available):
                    toggle_available_points()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_available:
                #print('click(down)')
                mx, my = pygame.mouse.get_pos()
                print(mx, my)
                for point in board.points:
                    if point.clicked_me(mx, my):
                        print('i,j=',point.i,point.j)
                        toggle_available_points()
                        board.insert((point.i, point.j), current_id)
                        board.update_components()
                        current_id = EMPTY_ID
                        mouse_component = 0

        manager.process_events(event)

    manager.update(time_delta)

    screen.blit(background, (0, 0))    
    screen.blit(board.surface, (210, 10))

    for com in board.components:
        screen.blit(com.surface, (210+com.posX, 10+com.posY))

    if show_available:
        for point in board.points:
            posX = (point.i+0.5)*board.gridWidth-point.rect.w/2+210
            posY = (point.j+0.5)*board.gridHeight-point.rect.h/2+10
            screen.blit(point.surface, (posX, posY))
            point.rect = pygame.Rect(posX, posY, POINT_SIZE, POINT_SIZE)

    if mouse_component != 0:
        screen.blit(mouse_component.surface, (mouse_rect.x, mouse_rect.y))
    #pygame.draw.rect(surface=screen, color=pygame.Color(0,0,0), rect=mouse_rect)

    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()