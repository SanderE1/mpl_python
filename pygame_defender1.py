"""
Pygame Defender first week
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
size = (800, 500)
screen = pygame.display.set_mode(size)

# set up sprite lists
all_sprites_list = pygame.sprite.Group()
 
pygame.display.set_caption("Defender 1")

# load the sounds:
laser_sound = pygame.mixer.Sound("laser5.ogg")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# our ship class
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("defender_ship.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 250
        self.updown = 0
        self.speed = 8

        

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png").convert()
        self.image2 = self.image # store copy here
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.speed = 5        
        self.min_size = 4
        self.max_size = self.image.get_size()[0]

    def make_long(self, new_size):
        self.image = pygame.transform.scale(self.image2, (new_size, self.size[1]))
            
        
        
 
ship = Ship()
all_sprites_list.add(ship)
bullets = []

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            # press space to fire
            if event.key == pygame.K_SPACE:
                laser_sound.play()
                bullet = Bullet()
                bullet.direction = 1
                rect = copy.copy(ship.rect) # copy of the ship's position
                rect[0] += ship.image.get_size()[0] # front of the ship
                rect[1] += int(ship.image.get_size()[1]/2) # middle of the ship
                bullet.rect = rect
                bullet.make_long(bullet.min_size)
                all_sprites_list.add(bullet)
                bullets.append(bullet)
                                
            # if the up or down key is pressed, set the direction of movement
            if event.key == pygame.K_UP:
                ship.updown = -1
            if event.key == pygame.K_DOWN:
                ship.updown = 1            
        if event.type == pygame.KEYUP:
            # when you stop pressing, stop moving!
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                ship.updown = 0
                

 
    # --- Game logic should go here
    ship.rect.y += (ship.speed * ship.updown)

    for bullet in bullets:
        if bullet.image.get_size()[0]<bullet.max_size:
            bullet.make_long(bullet.image.get_size()[0] + bullet.speed)
        else: bullet.rect.x += bullet.speed
        if bullet.rect.x > size[0]:
            bullets.remove(bullet)

    
 
    # --- Screen-clearing code goes here
    screen.fill(WHITE)
 
    # --- Drawing code should go here
    all_sprites_list.draw(screen)
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
