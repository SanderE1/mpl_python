"""
Asteroids!
"""
 
import pygame
import math

def rotatePoint(centerPoint,point,angle):
    """Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (600, 600)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
all_sprites_list = pygame.sprite.Group()
pygame.display.set_caption("Astroids")

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([26,26])
        self.pts = [[15, 0],[5,25], [15,15], [25,25]]
        pygame.draw.aalines(self.image, WHITE, True, self.pts,2)
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300
        self.angle = 0
        self.speed = 0

    def rotate(self, angle):
        for i, pt in enumerate(self.pts):
            self.pts[i] = rotatePoint([13,13], pt, angle)
        self.image.fill(BLACK)
        pygame.draw.lines(self.image, WHITE, True, self.pts,2)

    def get_direction(self):
        # we know pts[0] and pts[2] give us a vector we are "pointing" at:
        vector = [self.pts[0][0] - self.pts[2][0], self.pts[0][1] - self.pts[2][1]]
        # normalize:
        norm = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        vector = [vector[0] / norm, vector[1] / norm]
        return vector
        

ship = Ship()
all_sprites_list.add(ship)

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.angle = 1
            if event.key == pygame.K_LEFT:
                ship.angle = -1
            if event.key == pygame.K_UP:
                ship.speed = 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                ship.angle = 0
        
 
    # --- Game logic should go here

    if ship.angle != 0:
        ship.rotate(ship.angle)

    vect = ship.get_direction()
    ship.rect.x += (vect[0]*ship.speed)
    ship.rect.y += (vect[1]*ship.speed)

    # wrap ship:
    if ship.rect.x < 0:
        ship.rect.x = size[0]
    if ship.rect.x > size[0]:
        ship.rect.x = 0
    if ship.rect.y < 0:
        ship.rect.y = size[1]
    if ship.rect.y > size[1]:
        ship.rect.y = 0

    # decay speed:
    if ship.speed > 0:
        ship.speed -=0.1
    
    
    
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
 
    # --- Drawing code should go here
    all_sprites_list.draw(screen)
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
