import pygame
import pymunk
#to link the 2 libraries 
import pymunk.pygame_util


#initialize the pygame (modules, environment)
pygame.init()

#sizes of the game 
SCREEN_WIDTH = 1200 
SCREEN_HEIGHT = 678

#create a game window for displaying graphics 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pool Practier")


#pymunk space
space = pymunk.Space()
#to tell pymunk to draw the shapes that we created, otherwise it is not getting displayed 
draw_options = pymunk.pygame_util.DrawOptions(screen)

#function for creating balls 
#pymunk objects consist of body and shape (body is the center, shape is the surrounding)
def create_ball(radius, position):
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, radius)
    #unitless value: experiment with is, to find the right mass
    shape.mass = 5

    space.add(body)
    space.add(shape)
    return shape

newBall = create_ball(25, (300, 100))




#game loop, so the screen stays displayed 
run = True
while run == True: 
    for event in pygame.event.get():
        #pygame.QUIT is the X on the top right screen (^= closing the screen)
        if event.type == pygame.QUIT:
            run = False
    
    space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()