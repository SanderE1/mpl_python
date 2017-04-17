"""
Asteroids!
"""
 
import pygame
import math
import copy
import random
import os

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

shoot_sound = pygame.mixer.Sound('pew.wav')
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
all_sprites_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
score = 0
astroid_amount = 0

pygame.display.set_caption("Astroids")

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([26,26])
        self.pts = [[15, 0],[5,25], [15,15], [25,25]]
        pygame.draw.aalines(self.image, WHITE, True, self.pts,2)
        self.image.set_colorkey(BLACK)
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([2,2])
        self.image.fill(WHITE)
        self.speed = 5
        self.life = 0
        
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,50])
        self.pts = [[10,0],[20,10],[30,0],[40,10],[30,20],[40,30],[30,40],[20,45],[10,45],[0,30],[0,20]]
        pygame.draw.lines(self.image, WHITE, True, self.pts,2)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        x = random.randint(0,size[0])
        y = random.randint(0,size[1])
        self.rect.x = x
        self.rect.y = y
        self.direction = self.randomDirection()
        self.speed = random.randint(2,5)

    def randomDirection(self):
        randVect = [random.randint(-10,10),random.randint(-10,10)]
        norm = math.sqrt(randVect[0] ** 2 + randVect[1] ** 2)
        vector = [randVect[0] / norm, randVect[1] / norm]
        return vector

def wrap(sprite):
    if sprite.rect.x < 0:
        sprite.rect.x = size[0]
    elif sprite.rect.x > size[0]:
        sprite.rect.x = 0
    if sprite.rect.y < 0:
        sprite.rect.y = size[1]
    elif sprite.rect.y > size[1]:
        sprite.rect.y = 0
    
def updateScore(screen, score):
    message = "Score:{}".format(score)
    font = pygame.font.SysFont("Courier New", 30)
    text = font.render(message, False, WHITE)
    screen.blit(text, (10,10))
    
ship = Ship()
all_sprites_list.add(ship)
    

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
      if astroid_amount < 7:
        asteroid = Asteroid()
        all_sprites_list.add(asteroid)
        asteroids.add(asteroid)
        astroid_amount += 1
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
            if event.key == pygame.K_SPACE:
                shoot_sound.play()
                bullet = Bullet()
                bullet.rect = bullet.image.get_rect()
                bullet.rect = copy.copy(ship.rect)
                bullet.rect.x += ship.pts[0][0]
                bullet.rect.y += ship.pts[0][1]
                bullet.direction = ship.get_direction()
                bullets.add(bullet)
                all_sprites_list.add(bullet)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                ship.angle = 0
        
 
    # --- Game logic should go here

    # update the ship:
    if ship.angle != 0:
        ship.rotate(ship.angle)

    vect = ship.get_direction()
    ship.rect.x += (vect[0]*ship.speed)
    ship.rect.y += (vect[1]*ship.speed)
    wrap(ship)
    # decay speed:
    if ship.speed > 0:
        ship.speed -= 0.1
    if ship.speed < 0:
        ship.speed = 0

    # update all the bullets:
    for bullet in bullets:
        bullet.rect.x += (bullet.direction[0] * bullet.speed)
        bullet.rect.y += (bullet.direction[1] * bullet.speed)     
            
        wrap(bullet)
        
        bullet.life += 1
        if bullet.life > 100:
            bullets.remove(bullet)
            all_sprites_list.remove(bullet)

    # update all the asteroids:
    for asteroid in asteroids:
        asteroid.rect.x += (asteroid.direction[0] * asteroid.speed)
        asteroid.rect.y += (asteroid.direction[1] * asteroid.speed)
        wrap(asteroid)   


    # do we have any bullets coliding w/ asteroids?
    hit_dict = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    for asteroid in hit_dict.keys():
        score += 1
        astroid_amount -= 1
        print "score:{}".format(score)
    


    
    
    
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
 
    # --- Drawing code should go here
    all_sprites_list.draw(screen)
    updateScore(screen, score)
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
