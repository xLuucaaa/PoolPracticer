#########################################################  Libraries   ######################################################################
import pygame
import pymunk
#to link the 2 libraries 
import pymunk.pygame_util
######################################################### /Libraries   ######################################################################


#########################################################  Game-Setup   ######################################################################
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
#static body doesnt move/act to forces applied to it (is applied on the screen, so it never moves (represents the table))
static_body = space.static_body
#to tell pymunk to draw the shapes that we created, otherwise it is not getting displayed 
draw_options = pymunk.pygame_util.DrawOptions(screen)

#clock (time to update the screen) - update the screen 120 times per second
clock = pygame.time.Clock()
FPS = 120

#colors
background_color = (50, 50, 50)

#load images (.convert_alpha to make it look smoother)
table_image = pygame.image.load("images/table.png").convert_alpha()


#########################################################  /Game-Setup   ######################################################################



#########################################################  Functions   ######################################################################
#function for creating balls 
#pymunk objects consist of body and shape (body is the center, shape is the surrounding)
def create_ball(radius, position):
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, radius)
    #unitless value: experiment with is, to find the right mass
    shape.mass = 5
    #for bouncing back 
    shape.elasticity = 0.8
    #PivotJoint to allow 2 bodies to rotate around a common point: friction between poolball and pooltable 
                            #body a         b     anch    anch
    pivot = pymunk.PivotJoint(static_body, body, (0,0), (0,0))
    #diable joint correction 
    pivot.max_bias = 0  
    #emulate linear friction
    pivot.max_force = 1000

    space.add(body)
    space.add(shape)
    space.add(pivot)
    return shape

new_ball = create_ball(25, (300, 300))

cue_ball = create_ball(25, (600, 320))

#create one pool table cushion 
cushions = [
  [(88, 56), (109, 77), (555, 77), (564, 56)],
  [(621, 56), (630, 77), (1081, 77), (1102, 56)],
  [(89, 621), (110, 600),(556, 600), (564, 621)],
  [(622, 621), (630, 600), (1081, 600), (1102, 621)],
  [(56, 96), (77, 117), (77, 560), (56, 581)],
  [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]

#function for creating curshions (take the parameters (diameters of cushion))
def create_cushion(poly_dims):
    #static, because the cushions are fixed and do not move around
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = (0, 0)
    shape = pymunk.Poly(body, poly_dims)
    #for bouncing back
    shape.elasticity = 0.8
    space.add(body)
    space.add(shape)

for c in cushions:
    create_cushion(c)

#########################################################  /Functions   ######################################################################




#########################################################  MAIN LOOP GAME   ######################################################################
#game loop, so the screen stays displayed 
run = True
while run == True: 

    clock.tick(FPS)
    #physicswise: time that should ellapse between each frame - physics ^= clock ticks
    space.step(1 / FPS)

    #fill background 
    screen.fill(background_color)

    #draw pool table 
    screen.blit(table_image, (0,0))

    for event in pygame.event.get():
        #event when mouseclick, that the cueball (white) is moving
        if event.type == pygame.MOUSEBUTTONDOWN:
            #apply_impulse is a pymunk func....   imp x, y of white  | x, y coordinates relative to center of body 
            cue_ball.body.apply_impulse_at_local_point((-1000, 0), (0, 0))

        #pygame.QUIT is the X on the top right screen (^= closing the screen)
        if event.type == pygame.QUIT:
            run = False
    
    space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
#########################################################  /MAIN LOOP GAME   ######################################################################