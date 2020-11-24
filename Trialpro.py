import pygame
from pygame.locals import *
import sys
import random
import time

pygame.init()
 
vec = pygame.math.Vector2 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crap Tutorial")



############ Define Player class ############################
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((50, 400))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.score = 0
        self.jumping = False #######Tutorial has this both here and in the update definition. Seems redundant

##### update function. Used in main loop to update player values. ####################        
    def update(self):
        hits = pygame.sprite.spritecollide(self , platforms, False)
        if self.vel.y > 0:
           if hits:
               if self.pos.y < hits[0].rect.bottom:
                   if hits[0].point == True:
                       hits[0].point == False
                       self.score += 1 ################Check score loop. updates endlessly. Should only count +1 per platform
                   self.pos.y = hits[0].rect.top + 1
                   self.vel.y = 0
                   self.jumping = False
            
########## Move function. Used in while loop to give player mobility and feeling of gravity ###################
    def move(self):
        self.acc = vec(0,0.2)
    
        pressed_keys = pygame.key.get_pressed()            
        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC
             
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        self.rect.midbottom = self.pos

############### Jump function. Enables player to jump. Only when not already jumping##########
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -10

############# Cancel jump function. Allows for a quick jump ###############
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y <-4:
                self.vel.y = -4

##### Platform class ######               
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH -10), random.randint(0, HEIGHT - 30)))
        self.point = True
        self.speed = random.randint(-1, 1)
        self.moving = True
        
##### Supposed to enable platforms to move.... Cant make it work ######        
    def platmove(self):
        if self.moving == True:
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

####check platform grouping before generation #######
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
               continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
               return True
        C = False
        
####generate platforms if less than 6 are on screen        
def plat_gen():
    while len(platforms) < 6 :
        width = random.randrange(50,100)
        p = platform()
        C = True

        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))
            C = check(p, platforms)

        platforms.add(p)
        all_sprites.add(p)

#### Create platform PT1 disable points and motion
PT1 = platform()
PT1.point = False
PT1.moving = False
#####Create player P1
P1 = Player()                                       

#####Settings for PT1
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
                                    
####create all_sprites group and add PT1 and P1- apparently this is the easiest way to draw things(?) 
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

####Platforms is added to sprite group
#### dont understand why PT1 is being added here if its already in all sprites which belones to sprite group.
####Not really sure whats going on here. Platforms is only called in the update function when checking for collisions.
platforms = pygame.sprite.Group()
platforms.add(PT1)

###Initial platform generation######
for x in range(random.randint(4, 5)):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)

#####Main game loop#########    
while True:       
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                P1.jump()
        if event.type == pygame.KEYUP:
           if event.key == pygame.K_j:
               P1.cancel_jump()
####Game over condidion ########
    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill((0,0,255))
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            sys.exit()
#####Move screen when player approaches top third
    if P1.rect.top <= HEIGHT /3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT + 60:
                plat.kill()
######Display score##########
    displaysurface.fill((0,0,0))
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(P1.score), True, (123,255,0))
    displaysurface.blit(g, (WIDTH/2, 10))

####Call functions that require looping
    plat_gen()
    P1.move()
    P1.update()

###Draw anything in all_sprites####
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
    
    pygame.display.update()
    FramePerSec.tick(FPS)
