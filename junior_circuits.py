import pygame
import pygame_gui

from core.board import Board

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

board.insert((5,9), 1)
board.update_components()
#source = Component("assets/sprites/source.png")

manager = pygame_gui.UIManager(window_size)
manager.get_theme().load_theme("assets/themes/left_panel_theme.json")

# GUI Objects
left_panel_rect = pygame.Rect(-5, -5, 200, HEIGHT+15)
left_panel = pygame_gui.elements.UIPanel(relative_rect=left_panel_rect, manager=manager, object_id="#left_panel")

clock = pygame.time.Clock()
debug_mode = False
running = True

while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                debug_mode = ~debug_mode
                manager.set_visual_debug_mode(debug_mode)

        manager.process_events(event)

    manager.update(time_delta)

    screen.blit(background, (0, 0))    
    screen.blit(board.surface, (210, 10))
    #screen.blit(source.surface, (300, 300))

    for com in board.components:
        screen.blit(com.surface, (210+com.posX, 10+com.posY))

    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()