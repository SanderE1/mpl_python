"""
Let's make a bouncing ball
"""
 
import pygame
import copy

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False

# set up our ball
ball_pos = [350,250] # center of the screen
ball_size = 20
ball_direction = [1,1]
ball_max_speed = 10

# set up our ship
ship_pos = [350,450]
ship_direction = 0
ship_image = pygame.image.load("player.png").convert()
ship_image.set_colorkey(BLACK)

# how about some bullets?
bullets = []
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship_direction = -1
            if event.key == pygame.K_RIGHT:
                ship_direction = 1
            if event.key == pygame.K_SPACE:
                bullet_pos = copy.copy(ship_pos)
                bullet_pos[0] += 37
                bullets.append(bullet_pos)
 
    # --- Game logic should go here
    ''' I got tired of writing all this:
    if ball_pos[0]>size[0]:
        ball_direction[0] *= -1
    if ball_pos[1]>size[1]:
        ball_direction[1] *= -1
    if ball_pos[0] == 0:
        ball_direction[0] *= -1
    ball_pos[0] = ball_pos[0]+ball_direction[0]
    etc
    '''

    # We can do it all in a single for loop, efficiency!
    for i in [0,1]:
        if ball_direction[i] < ball_max_speed:
            ball_direction[i] *= 1.01
        if ball_pos[i] >= size[i] or ball_pos[i] <= 0:
            ball_direction[i] *= -1
        ball_pos[i] += int(ball_direction[i])
    
    # update ship location:
    ship_pos[0] += ship_direction
    if ship_pos[0]<1 or ship_pos[0]>650:
        ship_direction = 0
        
    # update bullets:
    for bullet in bullets:
        bullet[1] -= 1
        if bullet[0] < 1:
            bullets.remove(bullet)
            
    
    # --- Screen-clearing code goes here
    screen.fill(WHITE)
 
    # --- Drawing code should go here
    pygame.draw.circle(screen, BLACK, ball_pos, ball_size)
    screen.blit(ship_image, ship_pos)
    for bullet in bullets:
        pygame.draw.circle(screen, BLACK, bullet, 2)
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
