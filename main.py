#########################################################  Libraries   ######################################################################
import pygame
import math
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
BOTTOM_PANEL = 50

#create a game window for displaying graphics 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOM_PANEL))
pygame.display.set_caption("Pool Practicer")

#pymunk space
space = pymunk.Space()
#static body doesnt move/act to forces applied to it (is applied on the screen, so it never moves (represents the table))
static_body = space.static_body
#to tell pymunk to draw the shapes that we created, otherwise it is not getting displayed 
draw_options = pymunk.pygame_util.DrawOptions(screen)

#clock (time to update the screen) - update the screen 120 times per second
clock = pygame.time.Clock()
FPS = 120

#game variables 
lives = 3
diameter = 36
pocket_diameter = 66
force = 0
max_force = 13000
force_direction = 1
taking_shot = True
powering_up = False
cue_ball_potted = False
potted_balls = []
game_running = True


#colors
background_color = (50, 50, 50)
green_color = (0, 255, 0)
white_color = (255, 255, 255)

#fonts 
font = pygame.font.SysFont("Lato", 40)

large_font = pygame.font.SysFont("Lato", 60)


#load images (.convert_alpha to make it look smoother)
cue_image = pygame.image.load("images/cue.png").convert_alpha()
table_image = pygame.image.load("images/table.png").convert_alpha()
ball_images = []
for i in range(1, 17):
    # f works as a instring replacement 
    ball_image = pygame.image.load(f"images/ball_{i}.png").convert_alpha()
    ball_images.append(ball_image)


#########################################################  /Game-Setup   ######################################################################



#########################################################  Functions   ######################################################################

#function for outputting text onto the screen 
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


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

#setup game balls
balls = []
rows = 5
#potting balls
for col in range(5):
    for row in range(rows):
        pos = (250 + (col * (diameter+1)), 267 + (row * (diameter+1)) + (col * diameter / 2))
        new_ball = create_ball(diameter/2, pos)
        balls.append(new_ball)
    rows -= 1
#cue ball 
pos = (888, SCREEN_HEIGHT / 2)
cue_ball = create_ball(diameter / 2, pos)
balls.append(cue_ball)

#create 6 pockets on the table
pockets = [
  (55, 63),
  (592, 48),
  (1134, 64),
  (55, 616),
  (592, 629),
  (1134, 616)
]

#points that represent the corners of the cushions of the pool table
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


#create pool cue 
class Cue():
    def __init__(self, pos):
        self.original_image = cue_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    def update(self, angle):
        self.angle = angle

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, 
            (self.rect.centerx - self.image.get_width() / 2,
            self.rect.centery - self.image.get_height() / 2))

#balls[-1] to get the last item of the list (which is the cue ball)
cue = Cue(balls[-1].body.position)


#create powerbars to show how hard the cue ball will the hit
power_bar = pygame.Surface((10, 20))
power_bar.fill(green_color)


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

    #check, if any ball has been potted (each ball in every pocket)
    for i, ball in enumerate(balls):
        for pocket in pockets:
            ball_x_dist = abs(ball.body.position[0] - pocket[0])
            ball_y_dist = abs(ball.body.position[1] - pocket[1])
            #distance between center of the ball and the pocket
            ball_dist = math.sqrt((ball_x_dist ** 2)) + (ball_y_dist ** 2)
            if ball_dist <= pocket_diameter / 2:
                #check if the potted ball was the cue ball 
                if i == len(balls) - 1:
                    lives -= 1
                    cue_ball_potted = True

                    #remove the white ball 
                    ball.body.position = (-100, -100)
                    ball.body.velocity = (0.0, 0.0)

                else:
                    #remove the ball from the space 
                    space.remove(ball.body)
                    balls.remove(ball)
                    potted_balls.append(ball_images[i])
                    ball_images.pop(i)


    #draw pool balls (enumerate function can be used to also count the indexes)
    for i, ball in enumerate(balls):
                                    #position needed to be adapted: differences between pymunk and pygame
        screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

    #check if all the balls have stopped moving 
    taking_shot = True
    for ball in balls: 
        #make it integer to think about bugs: ball could move v=0.000001 m/s
        if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
            taking_shot = False


    #draw pool cue 
    #calculate pool cue angle 
    if taking_shot == True and game_running == True: 
        if cue_ball_potted == True:
            #reposition cue ball 
            balls[-1].body.position = (888, SCREEN_HEIGHT / 2)
            cue_ball_potted = False
        mouse_pos = pygame.mouse.get_pos()
        #center of the cue is set to the position of the cue ball 
        cue.rect.center = balls[-1].body.position
        x_dist = balls[-1].body.position[0] - mouse_pos[0]
        #y coordinate is flipped in pygame: invert it to make + to up 
        y_dist = -(balls[-1].body.position[1] - mouse_pos[1])
        #define the angle between the cue and the cue ball 
        cue_angle = math.degrees(math.atan2(y_dist, x_dist))
        cue.update(cue_angle)
        cue.draw(screen)

    #power up pool cue 
    if powering_up == True and game_running == True:
        force += 100 * force_direction
        if force >= max_force or force <= 0:
            force_direction *= -1
        #draw powerbars 
        for bar in range(math.ceil(force / 2000)):
            screen.blit(power_bar, (balls[-1].body.position[0] - 30 + (bar * 15), 
                        balls[-1].body.position[1] + 30))
            
    elif powering_up == False and taking_shot == True:
        x_impulse = math.cos(math.radians(cue_angle))
        y_impulse = math.sin(math.radians(cue_angle))
        #apply_impulse is a pymunk func....   imp x, y of white  | x, y coordinates relative to center of body 
        balls[-1].body.apply_impulse_at_local_point((force * -x_impulse, force * y_impulse), (0, 0))  
        #reset the force 
        force = 0  
        force_direction = 1

    #draw bottom panel 
    pygame.draw.rect(screen, background_color, (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL))
    draw_text("LIVES: " + str(lives), font, white_color, SCREEN_WIDTH -200, SCREEN_HEIGHT +10)

    #draw potted balls in bottom panel 
    for i, ball in enumerate(potted_balls):
        screen.blit(ball, (10 + (i * 50), SCREEN_HEIGHT + 10))

    #check for game over 
    if lives <= 0:
        draw_text("GAME OVER", large_font, white_color, SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2)
        game_running = False


    for event in pygame.event.get():
        #event when mouseclick, that the cueball (white) is moving
        if event.type == pygame.MOUSEBUTTONDOWN and taking_shot == True:
            powering_up = True
        if event.type == pygame.MOUSEBUTTONUP and taking_shot == True:
            powering_up = False
         

        #pygame.QUIT is the X on the top right screen (^= closing the screen)
        if event.type == pygame.QUIT:
            run = False
    
    #space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
#########################################################  /MAIN LOOP GAME   ######################################################################