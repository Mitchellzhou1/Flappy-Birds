import pygame
import sys
import random

# game Variables
gravity = .13
speed = 0
curr_score = -0.5
game_active = True
floor_position = 0
pipe_heights = [300, 350, 400, 450, 500]
##########################

pygame.init()

game_font = pygame.font.Font("04B_19.TTF", 70)

screen = pygame.display.set_mode((450, 800))
frames = pygame.time.Clock()

background = pygame.image.load("pictures/Background.png").convert()
background = pygame.transform.smoothscale(background, (450, 800))

ground = pygame.image.load("pictures/ground.png").convert()
ground = pygame.transform.scale2x(ground)

bird = pygame.image.load("pictures/red_bird.png").convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_surface = bird.get_rect(center=(100, 300))

pipes_surface = pygame.image.load("pictures/pipe.png").convert()
pipes_surface = pygame.transform.scale2x(pipes_surface)

main_menu = pygame.image.load("pictures/home.png").convert_alpha()
main_menu = pygame.transform.scale2x(main_menu)

NEWPIPE = pygame.USEREVENT
pygame.time.set_timer(NEWPIPE, 700)
pipeLst = []


def draw_floor(position_of_floor):
    """ creates the floor of the game """
    if position_of_floor == -190:
        screen.blit(ground, (0, 650))
        return 0
    screen.blit(ground, (position_of_floor, 650))
    position_of_floor -= 1
    return position_of_floor


def new_pipe():
    """ creates a new pipe and adds it to the pipe list """
    pipeHeight = random.choice(pipe_heights)
    top_pipe = pipes_surface.get_rect(midtop=(500, pipeHeight))
    bottom_pipe = pipes_surface.get_rect(midbottom=(500, pipeHeight - 200))
    return bottom_pipe, top_pipe


def draw_pipes(pipes):
    """displays the pipes onto the screen"""
    for pipe in pipes:
        screen.blit(pygame.transform.flip(pipes_surface, False, True), pipe[0])
        screen.blit(pipes_surface, pipe[1])
        pipe[0].centerx -= 5
        pipe[1].centerx -= 5
    if len(pipes) > 10:
        pipes.pop(0)
    return pipes


def collision_checker(pipe):
    """checks for the collision between the bird and the pipes"""
    if bird_surface.colliderect(pipe[0]) or bird_surface.colliderect(pipe[1]):
        return False
    elif bird_surface.top <= 0 or bird_surface.bottom >= 650:
        return False
    return True


def rotate_bird(bird):
    """ rotates the bird when it 'jumps' """
    return pygame.transform.rotozoom(bird, speed * 5, 1)


def display_score(score):
    """ displays the score onto the screen """
    if score < 0:
        score_text = game_font.render(str(0), True, (255, 255, 255))
    else:
        score_text = game_font.render(str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(450 / 2, 100))
    screen.blit(score_text, score_rect)


while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # exit button for the application window
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # hits space on keyboard
                if game_active:
                    speed = 0
                    speed -= 3.5
                else:
                    curr_score = -0.5
                    pipeLst = []
                    bird_surface.center = (100, 300)
                    speed = 0
                    game_active = True

        if event.type == NEWPIPE:
            pipeLst.append(new_pipe())

    # background
    screen.blit(background, (0, 0))

    if game_active:
        # bird movement
        speed += gravity
        up_flap = rotate_bird(bird)
        bird_surface.centery += speed
        screen.blit(up_flap, bird_surface)
        if pipeLst:
            game_active = collision_checker(pipeLst[-1])

        # pipes
        pipeLst = draw_pipes(pipeLst)
        curr_score += 1 / 67
        display_score(int(curr_score))
    else:
        screen.blit(main_menu, (40, 100))

    # ground
    floor_position = draw_floor(floor_position)

    pygame.display.update()
    frames.tick(100)
